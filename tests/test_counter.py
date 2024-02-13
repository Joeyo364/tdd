"""
Test Cases for Counter Web Service

Create a service that can keep a track of multiple counters
- API must be RESTful - see the status.py file. Following these guidelines, you can make assumptions about
how to call the web service and assert what it should return.
- The endpoint should be called /counters
- When creating a counter, you must specify the name in the path.
- Duplicate names must return a conflict error code.
- The service must be able to update a counter by name.
- The service must be able to read the counter
"""
from unittest import TestCase

# we need to import the unit under test - counter
from src.counter import app

# we need to import the file that contains the status codes
from src import status


class CounterTest(TestCase):
    """Counter tests"""
    def setUp(self):
        self.client = app.test_client()

    def test_create_a_counter(self):
        """It should create a counter"""
        client = app.test_client()
        result = client.post('/counters/foo')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

    def test_duplicate_a_counter(self):
        """It should return an error for duplicates"""
        result = self.client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        result = self.client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_409_CONFLICT)

    def test_update_a_counter(self):
        """It should read the counter"""
        counterName = 'testUpdate'
        counter, result = create_counter(counterName)  # create a counter
        self.assertEqual(result, status.HTTP_201_CREATED)  # ensure it was successful
        value = COUNTERS[counterName]  # check counters value as baseline
        result = update_counter(counterName)  # make a call to update counter
        self.assertEqual(result, status.HTTP_200_OK)  # ensure successful return code
        self.assertEqual(COUNTERS[counterName], value+1)  # check that counter was incremented

    def test_delete_a_counter(self):
        """It should delete a counter"""
        result = self.client.post('/counters/delete')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        result = self.client.delete('/counters/delete')
        self.assertEqual(result.status_code, status.HTTP_204_NO_CONTENT)


COUNTERS = {}


# We will use the app decorator and create a route called slash counters.
# specify the variable in route <name>
# let Flask know that the only methods that is allowed to called
# on this function is "POST".
@app.route('/counters/<name>', methods=['POST'])
def create_counter(name):
    """Create a counter"""
    app.logger.info(f"Request to create counter: {name}")
    global COUNTERS
    if name in COUNTERS:
        return {"Message": f"Counter {name} already exists"}, status.HTTP_409_CONFLICT
    COUNTERS[name] = 0
    return {name: COUNTERS[name]}, status.HTTP_201_CREATED


def update_counter(name):
    """It should update the counter"""
    COUNTERS[name] += 1
    return status.HTTP_200_OK
