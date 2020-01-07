curl -X GET http://0.0.0.0:8000/prediction/houses/

curl -X POST -H "Content-Type:application/json" -d\
 '{"CRIM": "12232", "ZN": 2.12, "INDUS": 3.12, "CHAS": 4.12, "NOX": 5.12, "RM": 6.12, "AGE": 7.12, "DIS": 8.12, "RAD": 9.12, "TAX": 10.12, "PTRATIO": 11.12, "B": 12.12, "LSTAT": 13.12, "MEDV": null}' \
 http://0.0.0.0:8000/prediction/houses/

curl -X GET http://0.0.0.0:8000/prediction/houses/2/

curl -X PUT -H "Content-Type:application/json" -d '{ "TAX": 9999 }' \
 http://0.0.0.0:8000/prediction/houses/11/ > reponse.html

 ## predictions
 curl -X POST -H "Content-Type:application/json" -d\
  '{"CRIM": "1", "ZN": 0, "INDUS": 0, "CHAS": 2, "NOX": 1, "RM": 2.3, "AGE": 7.12, "DIS": 8.12, "RAD": 9.12, "TAX": 10.12, "PTRATIO": 11.12, "B": 12.12, "LSTAT": 13.12, "MEDV": null}' \
  http://0.0.0.0:8000/prediction/predict/ > reponse.html
