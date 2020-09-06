
### Gmail Sentiment Analysis Tool
-[项目提案](https://docs.google.com/presentation/d/1-2Q3bgghBpHv-JMVL14N0cxV4HNiQBJ3ay32Xb0ETiw/edit?ts=5f53d799#slide=id.g9443376c3b_5_0)

-[项目demo](./zoom_0.mp4)

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
     ],
     "tones" : {
        {'Confident': 
            {'now': {'score': 0.92567, 'count': 1}}, 
        'Joy': 
            {'now': {'score': 0.557822, 'count': 1}},
        'Tentative': 
            {'now': {'score': 0.55795, 'count': 1}}, 
        'Analytical': 
            {'now': {'score':0.720783, 'count': 1}}, 
        'Sadness': 
            {'now': {'score': 0.538199, 'count': 1}}
        }
    }

 }

```




