from fastapi import APIRouter,HTTPException

router=APIRouter(prefix="/products",
                 tags=["products"],
                 responses={404:{"missing":"Producto no encontrado"}})

products_list =['producto 1','producto 2','producto 3','producto 4','producto 5']

@router.get("/")
async def products():
    return products_list

@router.get("/{id}")
async def products(id:int):
    
    try:
        return products_list[id]
    except:
        raise HTTPException(status_code=404)