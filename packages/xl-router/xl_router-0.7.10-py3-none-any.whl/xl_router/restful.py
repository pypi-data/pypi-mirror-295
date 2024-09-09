from typing import Optional


class R:
    @classmethod
    def get(cls, 
            id: Optional[int] = None, 
            order_by: Optional[str]=None, 
            page_num: Optional[int] = None, 
            page_size: Optional[int] = None, 
            **kwargs):
        if id:
            return cls.get_json(id)
        else:
            return cls.get_jsons(
                order_by=order_by, 
                page_num=page_num, 
                page_size=page_size,
                **kwargs
            )

    @classmethod
    def post(cls, data: dict):
        cls.add(data)

    @classmethod
    def put(cls, id: int, data: dict):
        cls.save(id, data)

    @classmethod
    def delete(cls, id: int):
        cls.delete_list(id=id)

   