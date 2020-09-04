### gmail api setup
```
python3 -m venv env
source env/bin/activate
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```



### file structure
```
--frontend
  --App.js (main file)
  --components
    --TextBox.js

--backend
  --env
  --index.js  (main server)
  --tone-analyzer.py (test file to interact with ibm api)
```

### front-end
```
cd front-end
npm install
npm start
```

### back-end
```
cd backend
python3 -m venv env
source env/bin/activate
pip install --upgrade "ibm-watson>=4.6.0"
python3 index.py
```

### endpoint
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



