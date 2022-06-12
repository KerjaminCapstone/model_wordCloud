# model_wordCloud
This is a REST API to connect our machine learning process into our main api. Like a word cloud in general, this endpoint produces most frequently found words in client reviews in the form of array. When the client post a review, our main api will get the array from this endpoint and store it to the database. The client can view list of this word cloud result in the freelance profile. 

![image](https://user-images.githubusercontent.com/83566398/173227140-616f9e9a-368a-432c-8c58-07617180ac7a.png)

# How to try this api?
You can try this api at https://word-cloud-api-dot-kerjamin-capstone.et.r.appspot.com/predict

### Header
```sh
Content-Type: application/json
```
### Body
```sh
{
    "id": <freelancer-id>,
}
```
### Response (result)
```sh
{
    "data": [
        {
            "sifat": <word-cloud-result-1>,
            "value": <count>
        },
        {
            "sifat": <word-cloud-result-2>,
            "value": <count>
        }
        ...
    ]
}
```

### Example
![image](https://user-images.githubusercontent.com/83566398/173227214-419ccc2f-924a-4367-9ada-84b87f73cf6e.png)
