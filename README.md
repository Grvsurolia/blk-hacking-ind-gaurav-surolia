# BlackRock Auto Saving Challenge

## Run locally

pip install -r requirements.txt
uvicorn app.main:app --port 5477

## Docker

docker build -t blk-hacking-ind-gaurav-surolia .
docker run -p 5477:5477 blk-hacking-ind-gaurav-surolia

## Endpoints

/transactions:parse  
/transactions:validator  
/transactions:filter  
/returns:nps  
/returns:index  
/performance  

## Design

System supports up to 1 million transactions using efficient temporal processing.

## Tests

pytest