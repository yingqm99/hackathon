###front-end
```
cd front-end
npm install
npm start
```

###back-end
```
cd backend
python3 -m venv env
source env/bin/activate
pip install --upgrade "ibm-watson>=4.6.0"
python3 index.py
```

###endpoint
```
localhost:3000
:/   
:/test

:/emails
 [
     {emailid: "",
      date: "",
      content: ""},
     ...
 ]

:/email/date=?
 [
     {emailid: "",
      sore: "",
      tone: ""},
     ...
 ]


```



