from fastapi import APIRouter
from starlette.responses import JSONResponse
from fastapi_mail import FastMail, MessageType

from utils.email_utils import conf, MessageSchemaDefinition
from utils.email_utils import EmailSchema


router = APIRouter(prefix="/test",
                   tags=["test"],
                   responses={200: {"description": "Welcome on users route"}},
                   )


@router.post("/email")
async def simple_send(email: EmailSchema) -> JSONResponse:
    html = "<p>Thanks for using </p>"
    message = MessageSchemaDefinition(email.email,
                                      "Message Object",
                                      html,
                                      MessageType.html)
    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200,
                        content={"message": "email has been sent"})
