''' 
Use cases are the core of the application. They are the classes 
that contain the business logic of the application. 
'''

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

Input = TypeVar('Input')
Output = TypeVar('Output')


class UseCase(Generic[Input, Output], ABC): # pylint: disable=too-few-public-methods
    ''' Use Case Interface '''

    @abstractmethod
    def execute(self, input_param: Input) -> Output:
        ''' Execute the use case'''
        raise NotImplementedError()
