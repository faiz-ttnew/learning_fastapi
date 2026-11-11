from fastapi import HTTPException
from sqlalchemy import text, bindparam

from app.common.enums import UserRole
from app.db.database import engine
from app.schemas.auth_schema import UserResponse
from app.schemas.ticket_schema import (
    TicketCreate, 
    TicketResponse, 
    TicketUpdate,
    TicketDetailWithAssignedUser,
    TicketFilter
)
from app.services import auth_service
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
import json
from app.common.pagination import PaginationSchema

TICKET_SELECT = """
    SELECT id, title, description, status, priority,
           created_by, assigned_to, created_at, updated_at
    FROM tickets
"""

TICKET_DETAIL_SELECT = """
    SELECT
        t.id, t.title, t.description, t.status, t.priority,
        t.created_by, t.assigned_to, t.created_at, t.updated_at,
        CASE
            WHEN u.id IS NULL THEN NULL
            ELSE JSON_OBJECT(
                'id', u.id,
                'name', u.name,
                'email', u.email
            )
        END AS assigned_to
    FROM tickets AS t
    LEFT JOIN users AS u ON u.id = t.assigned_to
"""

def row_to_ticket_detail(row) -> TicketDetailWithAssignedUser:
    data = dict(row)

    # text() query mein JSON column string (ya bytes) aata hai, dict nahi
    if isinstance(data["assigned_to"], (str, bytes, bytearray)):
        data["assigned_to"] = json.loads(data["assigned_to"])

    return TicketDetailWithAssignedUser.model_validate(data)


def create_ticket(data: TicketCreate, user_id: int) -> TicketResponse:
    with engine.begin() as conn:
        result = conn.execute(
            text("""
                insert into tickets (title, description, priority, created_by)
                values (:title, :description, :priority, :created_by)
            """),
            {
                "title": data.title,
                "description": data.description,
                "priority": data.priority.value,
                "created_by": user_id
            }
        )
        row = conn.execute(
            text(TICKET_SELECT + " WHERE id = :id"),
            {"id": result.lastrowid},
        ).mappings().one()

        return TicketResponse.model_validate(dict(row))

def get_tickets(current_user: UserResponse, paginate: PaginationSchema, filters: TicketFilter):
    query = TICKET_DETAIL_SELECT
    params ={"skip": paginate.skip, "limit": paginate.limit}
    conditions = []
    joins = ""

    if current_user.role != UserRole.ADMIN:
        query += " where created_by = :user_id"
        params["user_id"] = current_user.id

    values = filters.model_dump(exclude_none=True, mode="json")

    if "title" in values:
        conditions.append("t.title like :title")
        params["title"] = f"%{values['title']}%"

    if "created_by_name" in values:
        joins += " JOIN users as c on c.id = t.created_by"
        conditions.append("c.name like :created_by_name")
        params["created_by_name"] = f"%{values['created_by_name']}%"

        query += "u.name"

    for column in ("status", "priority", "assigned_to"):
        if column in values:
             conditions.append(f"t.{column} = :f_{column}")
             params[f"f_{column}"] = values[column]
    
    query = TICKET_DETAIL_SELECT + joins

    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    query += " ORDER BY t.id DESC LIMIT :limit OFFSET :skip"

    with engine.connect() as conn:
        rows = conn.execute(text(query), params).mappings().all()

    return [row_to_ticket_detail(r) for r in rows]

def get_ticket(ticket_id: int, current_user: UserResponse) -> TicketResponse:
    user_id = current_user.id
    with engine.connect() as conn:
        row = conn.execute(
            text(TICKET_SELECT + " where id = :id and created_by = :created_by"),
            {"id": ticket_id, "created_by": user_id}
        ).mappings().one_or_none()

    return TicketResponse.model_validate(dict(row))

def get_ticket_by_id(ticket_id: int) -> TicketResponse:
    with engine.connect() as conn:
        row = conn.execute(
            text(TICKET_SELECT + " where id = :id"),
            {"id": ticket_id}
        ).mappings().one_or_none()

    return TicketResponse.model_validate(dict(row))

def assign_ticket(ticket_id: int, assignee_id: int) -> TicketResponse:
    ticket_data = get_ticket_by_id(ticket_id=ticket_id)

    user_data = auth_service.get_auth_user_by_id(assignee_id)

    if not ticket_data or not user_data:
        raise HTTPException(status_code=404, detail="Assignee or Ticket not found or Assignee account is inactive")

    with engine.begin() as conn:
        conn.execute(
            text("UPDATE tickets SET assigned_to = :a WHERE id = :id"),
            {"a": assignee_id, "id": ticket_id},
        )

        row = conn.execute(
            text(TICKET_SELECT + " WHERE id = :id"),
            {"id": ticket_id},
        ).mappings().one()

        return TicketResponse.model_validate(dict(row))

def update_ticket(
    ticket_id: int,
    data: TicketUpdate,
    current_user: UserResponse,
) -> TicketResponse:
    # Ticket exists or not -> 404
    get_ticket(ticket_id, current_user)

    # only send valid tickets (enum -> plain string)
    fields = data.model_dump(exclude_unset=True, mode="json")

    if "status" in fields and current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=403,
            detail="Only admin can change ticket status",
        )

    # Column names Pydantic model ke fixed fields se aate hain, user input se nahi,
    # isliye ye dynamic SET clause safe hai.
    set_clause = ", ".join(f"{column} = :{column}" for column in fields)
    params = {**fields, "id": ticket_id}

    with engine.begin() as conn:
        conn.execute(
            text(f"UPDATE tickets SET {set_clause} WHERE id = :id"),
            params,
        )
        row = conn.execute(
            text(TICKET_SELECT + " WHERE id = :id"),
            {"id": ticket_id},
        ).mappings().one()

    return TicketResponse.model_validate(dict(row))

def delete_ticket(ticket_id: int, current_user: UserResponse) -> None:
    query = """
        DELETE FROM tickets
        WHERE id = :id AND created_by = :user_id
    """
    params = {"id": ticket_id, "user_id": current_user.id}

    try:
        with engine.begin() as conn:
            result = conn.execute(text(query), params)
    except IntegrityError as exc:
        # 1451: koi dusri table is ticket ko reference kar rahi hai
        if exc.orig.args[0] == 1451:
            raise HTTPException(
                status_code=409,
                detail="Ticket is in use and cannot be deleted",
            ) from exc
        raise
    except SQLAlchemyError as exc:
        raise HTTPException(
            status_code=500,
            detail="Could not delete ticket",
        ) from exc

    # 0 rows: ticket exist nahi karta ya is user ka nahi hai -> 404
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Ticket not found")

def bulk_assign_tickets(
    ticket_ids: list[int],
    assignee_id: int,
) -> list[TicketResponse]:
    with engine.begin() as conn:
        assignee = conn.execute(
            text("SELECT id, is_active FROM users WHERE id = :id"),
            {"id": assignee_id},
        ).mappings().one_or_none()

        if assignee is None:
            raise HTTPException(status_code=404, detail="Assignee user not found")
        if not assignee["is_active"]:
            raise HTTPException(status_code=400, detail="Assignee account is inactive")

        result = conn.execute(
            text("UPDATE tickets SET assigned_to = :a WHERE id IN :ids")
            .bindparams(bindparam("ids", expanding=True)),
            {"a": assignee_id, "ids": ticket_ids},
        )

        # Koi ticket exist nahi karta -> exception transaction ko rollback kar deta hai,
        # yaani koi bhi ticket assign nahi hota.
        if result.rowcount != len(ticket_ids):
            raise HTTPException(
                status_code=404,
                detail="One or more tickets not found",
            )

        rows = conn.execute(
            text(TICKET_SELECT + " WHERE id IN :ids ORDER BY id")
            .bindparams(bindparam("ids", expanding=True)),
            {"ids": ticket_ids},
        ).mappings().all()

        return [TicketResponse.model_validate(dict(row)) for row in rows]
