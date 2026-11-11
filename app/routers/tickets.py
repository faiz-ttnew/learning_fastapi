from fastapi import APIRouter, Depends, Query, status

from app.dependencies.auth import get_current_user, require_admin
from app.schemas.api_response import APIResponse, ResponseData
from app.schemas.auth_schema import UserResponse
from app.schemas.ticket_schema import (
    TicketAssign, 
    TicketCreate, 
    TicketResponse, 
    TicketUpdate,
    TicketBulkAssign,
    TicketFilter
)
from app.services import ticket_service
from app.common.pagination import PaginationSchema

router = APIRouter(
    prefix="/tickets", 
    tags=["Tickets"]
)

@router.post(
    "", 
    response_model=APIResponse[TicketResponse],
    status_code=status.HTTP_201_CREATED
)
def create_ticket(
    ticket: TicketCreate,
    current_user: UserResponse = Depends(get_current_user),
):
    created = ticket_service.create_ticket(ticket, current_user.id)
    return APIResponse[TicketResponse](
        success=True,
        data=ResponseData[TicketResponse](message="Ticket created successfully", data=created),
    )

@router.get("", response_model=APIResponse[list[TicketResponse]])
def list_tickets(
    filters: TicketFilter = Depends(),
    pagination: PaginationSchema = Depends(),
    current_user: UserResponse = Depends(get_current_user),
):
    tickets = ticket_service.get_tickets(current_user, pagination, filters)
    return APIResponse[list[TicketResponse]](
        success=True,
        data=ResponseData[list[TicketResponse]](message="", data=tickets),
    )

@router.get("/{ticket_id}", response_model=APIResponse[TicketResponse])
def get_ticket(
    ticket_id: int,
    current_user: UserResponse = Depends(get_current_user),
):
    ticket = ticket_service.get_ticket(ticket_id, current_user)
    return APIResponse[TicketResponse](
        success=True,
        data=ResponseData[TicketResponse](message="", data=ticket),
    )

@router.patch(
    "/{ticket_id}/assign",
    response_model=APIResponse[TicketResponse],
    dependencies =[Depends(require_admin)],   # admin-only
)
def assign_ticket(ticket_id: int, body: TicketAssign):
    ticket = ticket_service.assign_ticket(ticket_id, body.assigned_to)
    return APIResponse[TicketResponse](
        success=True,
        data=ResponseData[TicketResponse](message="Ticket assigned successfully", data=ticket),
    )

@router.patch(
    "/bulk-assign",
    response_model=APIResponse[list[TicketResponse]],
    dependencies=[Depends(require_admin)],
)
def bulk_assign_tickets(body: TicketBulkAssign):
    tickets = ticket_service.bulk_assign_tickets(body.ticket_ids, body.assigned_to)
    return APIResponse[list[TicketResponse]](
        success=True,
        data=ResponseData[list[TicketResponse]](
            message="Tickets assigned successfully",
            data=tickets,
        ),
    )

@router.patch("/{ticket_id}", response_model=APIResponse[TicketResponse])
def update_ticket(
    id: int,
    body: TicketUpdate,
    current_user: UserResponse = Depends(get_current_user),
):
    ticket = ticket_service.update_ticket(id, body, current_user)

    return APIResponse[TicketResponse](
        success=True,
        data=ResponseData[TicketResponse](
            message="Ticket updated successfully",
            data=ticket,
        ),
    )

@router.delete(
    "/{ticket_id}",
    response_model=APIResponse[dict]
)
def delete_ticket(
    ticket_id: int,
    current_user: UserResponse = Depends(get_current_user)
):
    ticket_service.delete_ticket(ticket_id, current_user)

    return APIResponse[dict](
        success=True,
        data=ResponseData[dict](
            message="Ticket deleted successfully",
            data={}
        )
    )
