from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def products(): ...

@router.get("/{name}")
def search_by_name(): ...

@router.post("/")
def filter(): ...

@router.post("/new")
def new_product(): ...