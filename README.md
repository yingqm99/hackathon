

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
npm install d3
npm install react-chartkick chart.js
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

### gmail api setup
in the virtual enviroment ^
```
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
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

:/email
 {
     "data" : [
         {
             "date": "",
             "emailod" : "",
             "score": "",
             "tone": ""
         },
         ...
     ]
 }
 
 
 :/recent_emotions
{
 "data":[{
          "tone_name" : str,
          "count" : int
          },
        ...,]
 }


 :/change_of_emotions
 {
 "data":[{
          'tone_name': str,
          'change': float,
          'most_recent_date': int
          },
        ...,]
  }
  
  
  :/personal_relations
  {
    "data":[{
          'person_name': str,
          'score': int,
          },
          ...,]
  }


```




