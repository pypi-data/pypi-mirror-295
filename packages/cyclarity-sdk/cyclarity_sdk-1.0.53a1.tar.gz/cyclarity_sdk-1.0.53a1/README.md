

CyClarity SDK
 
Introduction
 
CyClarity SDK is a Python package that provides an interface for interacting with the CyClarity platform. It includes classes and methods for creating, managing, and interacting with various resources on the platform.


Installation
 
You can install the CyClarity SDK using pip:

pip install cyclarity-sdk  
 

Usage
 
Here are examples of how to use the classes in the CyClarity SDK.
Runnable
The Runnable class is a base class for creating objects that can be run with setup and teardown phases. It has setup, run, and teardown methods that need to be implemented. Here is an example:

from cyclarity_sdk.runnable import Runnable, BaseResultsModel  
  
class MyResult(BaseResultsModel):  
    res_str: str  
  
class MyRunnable(Runnable[MyResult]):  
    desc: str  
    cli_args: str  
  
    def setup(self):  
        self.logger.info("Setting up")  
  
    def run(self):  
        self.logger.info("Running")  
        self.platform_api.send_test_report_description("This is a test description")  
        return MyResult(res_str="success!")  
  
    def teardown(self, exception_type, exception_value, traceback):  
        self.logger.info("Tearing down")  
 
To use this Runnable, you would do:

input = {  
    "desc": "test",  
    "cli_args": "-as -fsd -dsd",  
}  
  
with MyRunnable(**input) as runnable_instance:  # noqa  
    result: MyResult = runnable_instance()  
  
    # generates result json object  
    print("\ndictionary running results: ")  
    print(result.model_dump_json())  
 

PlatformApi
 
The PlatformApi class provides methods for interacting with the CyClarity platform. It is used within a Runnable instance through self.platform_api attribute. Here are the methods it supports:

send_test_report_description(description): This method sends a test report description to the platform.
send_finding(pt_finding): This method sends a finding to the platform.
send_execution_state(percentage, status, error_message): This method sends the execution state to the platform.

Here is how you might use PlatformApi in a Runnable:

class MyRunnable(Runnable[MyResult]):  
    desc: str  
    cli_args: str  
  
    def setup(self):  
        self.logger.info("Setting up")  
  
    def run(self):          self.logger.info("Running")  
        self.platform_api.send_test_report_description("This is a test description")  
        return MyResult(res_str="success!")  
  
    def teardown(self, exception_type, exception_value, traceback):  
        self.logger.info("Tearing down")  
 

Documentation
 
For more detailed information about deploying this test to the system,
please refer to the official documentation.