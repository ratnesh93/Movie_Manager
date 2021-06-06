import requests

data=[
  {
    "name": "Movie Test Data1",
    "image": "test url",
    "description": "test description",
    "dateLastEdited": "2018-05-19T12:33:25.545Z"
  },
  {
    "name": "Movie Test Data2",
    "image": "test url",
    "description": "test description",
    "dateLastEdited": "2017-11-28T04:59:13.759Z"
  },
  {
    "name": "The Movie Test Data3",
    "image": "test url",
    "description": "test description",
    "dateLastEdited": "2018-07-27T21:33:53.485Z"
  }]

update_data=  [{
    "oldtitle":"Movie Test Data1",
    "name": "updating Movie Test Data1",
    "image": "test url",
    "description": "test description"
  },
  {
    "oldtitle":"random test data",
    "name": "random name",
    "image": "test url",
    "description": "test description"
  }
  ]

BASE = "http://127.0.0.1:5000/"

class MyTest:
      
      #1: testing posting new movie
      def testPost(self):
          print("-----------------Testing "+BASE+"/movie"+"-----------------")
          for i in range(len(data)):
              response = requests.post(BASE + "movie",data[i])
              assert response.status_code==201
          print("-----------------Passed-----------------")
      
      #2: testing posting aldreay existing movie
      def testDuplicatePost(self):
          print("-----------------Testing duplicate POST "+BASE+"/movie"+"-----------------")
          response = requests.post(BASE + "movie",data[0])
          assert response.status_code==409
          print("-----------------Passed-----------------")
        
      #3: testing to update movie
      def testUpdate(self):
          print("-----------------Testing Update "+BASE+"/movie/update"+"-----------------")
          response = requests.post(BASE + "movie/update",update_data[0])
          assert response.status_code==200
          print("-----------------Passed-----------------")

      #4: testing updating movie with invalid movie name
      def testInvalidUpdate(self):
          print("-----------------Testing Invalid Update-----------------")
          response = requests.post(BASE + "movie/update",update_data[1])
          assert response.status_code==404
          print("-----------------Passed-----------------")
      
      #5 : testing normal search for movie
      def testSearch(self):
          print("-----------------Testing "+BASE+"/movie/search"+"-----------------")
          response = requests.post(BASE+"movie/search",{"name": "movie test"})
          assert response.status_code==200
          print("-----------------Passed-----------------")
      
      #6 : testing advance search for movie conating any of the search string
      def testAdvanceSearchAny(self):
          print("-----------------Testing "+BASE+"/movie/advanceSearchAny"+"-----------------")
          response = requests.post(BASE+"movie/advanceSearchAny",{"name": "movie test"})
          assert response.status_code==200
          print("-----------------Passed-----------------")
        
      #7 : testing normal search for movie conating all of the search string
      def testAdvanceSearchAll(self):
          print("-----------------Testing "+BASE+"/movie/advanceSearchAll"+"-----------------")
          response = requests.post(BASE+"movie/advanceSearchAll",{"name": "movie test the"})
          assert response.status_code==200
          print("-----------------Passed-----------------")

      #8: testing deleting movie
      def testDelete(self):
          print("-----------------Testing "+BASE+"/movie/delete"+"-----------------")
          response = requests.post(BASE + "movie/delete",{"name": update_data[0]['name']})
          assert response.status_code==200

          for i in range(1,len(data)):
              response = requests.post(BASE+"movie/delete",{"name": data[i]['name']})
              assert response.status_code==200
          
          print("-----------------Passed-----------------")
      
      #9 : testing delete for invalid movie
      def testInvalidDelete(self):
          print("-----------------Testing invalid delete"+BASE+"/movie/delete"+"-----------------")
          response = requests.post(BASE+"movie/delete",{"name": "random test data"})
          assert response.status_code==404
          print("-----------------Passed-----------------")

      #10: testing get response
      def testGetMovie(self):
          print("-----------------Testing "+BASE+"/movie"+"-----------------")
          response=requests.get(BASE+"movie")
          assert response.status_code==200
          print("-----------------Passed-----------------")
      
      #11: testing get response
      def testGetMovieAll(self): 
          print("-----------------Testing "+BASE+"/movie/all"+"-----------------")
          response=requests.get(BASE+"movie/all")
          assert response.status_code==200
          print("-----------------Passed-----------------")
        
      #12 : testing generating pdf
      def testGeneratePdf(self):
          print("-----------------Testing "+BASE+"/movie/generatePdf"+"-----------------")
          response = requests.post(BASE+"movie/generatePdf")
          assert response.status_code==200
          print("-----------------Passed-----------------")

def testMethods():
    test= MyTest()
    test.testPost()
    test.testDuplicatePost()
    test.testUpdate()
    test.testInvalidUpdate()
    test.testSearch()
    test.testAdvanceSearchAny()
    test.testAdvanceSearchAll()
    test.testDelete()
    test.testInvalidDelete()
    test.testGetMovie()
    test.testGetMovieAll()
    test.testGeneratePdf()

if __name__=='__main__':
    testMethods()





