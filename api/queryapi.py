from fastapi import APIRouter , Form 
from services.rag import rag

router = APIRouter()

rag_chain = rag()

@router.post('/chat')
async def query_pdf(query:str = Form(...)):
    response = rag_chain.generate_answers(query=query)
    return {'response': response}