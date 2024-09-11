'''
Created on September 20, 2021
@author: lwoydziak
'''
from json import loads

from mockito.matchers import any, Contains, And, ArgThat, Eq
from mockito.mocking import mock
from mockito.mockito import verify, when
from pytest import raises
from requests.exceptions import SSLError

from xenon_view_sdk import Xenon, ApiException

apiKey = '<apiKey>'
apiUrl = '<apiUrl>'


def setup_function(function):
    Xenon(apiKey=apiKey, apiUrl=apiUrl)


def teardown_function(function):
    Xenon._instance = None


def test_viewHeartbeatAdded():
    requests = mock()
    response = mock()
    response.status_code = 200
    when(requests).post('https://<apiUrl>/heartbeat', data=any(), headers=any(), verify=False).thenReturn(response)
    when(response).json().thenReturn({'result': 'success'})
    Xenon().featureCompleted('test')
    Xenon().heartbeat(PostMethod=requests.post, sleepTime=0, verify=False)

    def matchesHeartbeatApiParameters(arg):
        apiArguments = loads(arg)
        parameters = apiArguments['parameters']
        assert Eq("ApiHeartbeat").matches(apiArguments['name'])
        assert Eq('Feature').matches(parameters['journey'][0]['category'])
        assert any(float).matches(parameters['journey'][0]['timestamp'])
        assert any(str).matches(parameters['uuid'])
        assert any(float).matches(parameters['timestamp'])
        return True

    verify(requests).post('https://<apiUrl>/heartbeat',
                          data=ArgThat(matchesHeartbeatApiParameters),
                          headers={'Authorization': 'Bearer <apiKey>'},
                          verify=False)
    assert Xenon().journey() == []

def test_viewHeartbeatAddedWithWatchdog():
    requests = mock()
    response = mock()
    response.status_code = 200
    when(requests).post('https://<apiUrl>/heartbeat', data=any(), headers=any(), verify=False).thenReturn(response)
    when(response).json().thenReturn({'result': 'success'})
    Xenon().heartbeat(watchdog={'remove': True}, PostMethod=requests.post, sleepTime=0, verify=False)

    def matchesHeartbeatApiParameters(arg):
        apiArguments = loads(arg)
        parameters = apiArguments['parameters']
        assert Eq({'remove': True}).matches(parameters['watchdog'])
        return True

    verify(requests).post('https://<apiUrl>/heartbeat',
                          data=ArgThat(matchesHeartbeatApiParameters),
                          headers={'Authorization': 'Bearer <apiKey>'},
                          verify=False)
    assert Xenon().journey() == []

def test_viewHeartbeatAddedWithPlatform():
    requests = mock()
    response = mock()
    response.status_code = 200
    when(requests).post('https://<apiUrl>/heartbeat', data=any(), headers=any(), verify=False).thenReturn(response)
    when(response).json().thenReturn({'result': 'success'})
    Xenon().featureCompleted('test')
    softwareVersion = "5.1.5"
    deviceModel = "Pixel 4 XL"
    operatingSystemVersion = "12.0"
    operatingSystemName = "Android"
    Xenon().platform(softwareVersion, deviceModel, operatingSystemName, operatingSystemVersion)
    Xenon().heartbeat(PostMethod=requests.post, sleepTime=0, verify=False)

    def matchesHeartbeatApiParameters(arg):
        apiArguments = loads(arg)
        parameters = apiArguments['parameters']
        assert 'platform' in parameters.keys()
        return True

    verify(requests).post('https://<apiUrl>/heartbeat',
                          data=ArgThat(matchesHeartbeatApiParameters),
                          headers={'Authorization': 'Bearer <apiKey>'},
                          verify=False)
    assert Xenon().journey() == []


def test_viewHeartbeatFailsWithOneSslError():
    requests = mock()
    response = mock()
    response.status_code = 200
    when(requests).post('https://<apiUrl>/heartbeat', data=any(), headers=any(), verify=False).thenRaise(
        SSLError).thenReturn(response)
    when(response).json().thenReturn({'result': 'success'})
    Xenon().featureCompleted('test')
    Xenon().heartbeat(PostMethod=requests.post, sleepTime=0, verify=False)
    verify(requests, times=2).post('https://<apiUrl>/heartbeat',
                                   data=And([Contains('{"name": "ApiHeartbeat", "parameters": '),
                                             Contains('{"journey": [{"category": "Feature", "action": "Completed"'),
                                             Contains('}], "uuid":')]),
                                   headers={'Authorization': 'Bearer <apiKey>'},
                                   verify=False)
    assert Xenon().journey() == []


def test_viewHeartbeatFailsWithOneError():
    requests = mock()
    response = mock()
    response.status_code = 200
    when(requests).post('https://<apiUrl>/heartbeat', data=any(), headers=any(), verify=False).thenRaise(
        Exception).thenReturn(response)
    when(response).json().thenReturn({'result': 'success'})
    Xenon().featureCompleted('test')
    Xenon().heartbeat(PostMethod=requests.post, sleepTime=0, verify=False)
    verify(requests, times=2).post('https://<apiUrl>/heartbeat',
                                   data=And([Contains('{"name": "ApiHeartbeat", "parameters": '),
                                             Contains('{"journey": [{"category": "Feature", "action": "Completed"'),
                                             Contains('}], "uuid":')]),
                                   headers={'Authorization': 'Bearer <apiKey>'},
                                   verify=False)
    assert Xenon().journey() == []


def test_viewHeartbeatFails():
    requests = mock()
    response = mock()
    response.status_code = 400
    when(requests).post('https://<apiUrl>/heartbeat', data=any(), headers=any(), verify=False).thenReturn(response)
    when(response).json().thenReturn({'result': 'failed'})
    with raises(ApiException) as e:
        Xenon().featureCompleted('test')
        Xenon().heartbeat(PostMethod=requests.post, sleepTime=0, verify=False)

    assert Contains('Api responded with error.').matches(str(e.exconly()))
    journey = Xenon().journey()[0]
    assert journey['category'] == 'Feature'
    assert journey['timestamp'] > 0.0


def test_WhenViewHeartbeatFailsExceptionContainsResponse():
    requests = mock()
    response = mock()
    response.status_code = 400
    when(requests).post('https://<apiUrl>/heartbeat', data=any(), headers=any(), verify=False).thenReturn(response)
    when(response).json().thenReturn({'result': 'failed'})
    try:
        Xenon().featureCompleted('test')
        Xenon().heartbeat(PostMethod=requests.post, sleepTime=0, verify=False)
    except ApiException as e:
        assert e.apiResponse().status_code == response.status_code
