def send_response(status_code:int,response:any) -> dict:
  return {"status":status_code,"response":response}