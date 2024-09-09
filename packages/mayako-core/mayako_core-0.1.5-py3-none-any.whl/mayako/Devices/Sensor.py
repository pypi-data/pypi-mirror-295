from typing import Callable
from typing import List, TypeVar, Generic, Dict
from queue import Queue

from .Device import Device
from ..Models.SensorCapabilities import SensorCapabilities
from ..Models.BaseDataModel import BaseDataModel
from ..MayakoData import MayakoData
from ..Config import CCLIENT

#a generic type which is a subclass of BaseDataModel - a sensor data model class
T = TypeVar("T", bound=BaseDataModel)

class Sensor(Generic[T], Device):

    """
    this class represents a sensor on the remote microcontroller

    this class lets the user read and modify the capabilities of a sensor and subscribe OR/AND read sensor data. this class may not directly be instantiated! use "use_sensor()" method from the microcontroller class instead.

    Attributes:
        _data (Queue[T]): holds data until a user consumes it; uses the modelclass that is passed when this sensor was created
        _callback_functions (List[Callable[[T], None]]): the callback functions called when new data is available; function parameter is of type T
        _sensor_data_callback_identity (str): this is a unique key throughout the project which consists of the terms DATA, MC_IDENTITY and SENSOR_IDENTITY. this is used for the model class to specifically call this instance when new sensor data is available for it.
    """

    _data: Queue[T]
    _callback_functions: List[Callable[[List[T]], None]]
    _sensor_data_callback_identity: str

    def __init__(self, sensor_identity: str, mc_identity: str, model: MayakoData, sensor_class_type: T) -> None:
        super().__init__(identity=sensor_identity, mc_identity=mc_identity, model=model)
        self._sensor_class_type = sensor_class_type
        self._check_capabilities(sensor_identity=self._identity)
        self._sensor_data_callback_identity = f"DATA_{self._mc_identity}_{self._identity}"
        self._data = Queue()
        self._callback_functions = []
        self._subscribe_to_data()

    def get_data(self) -> List[T]:
        """
        retrieve data that is associated with this sensor if available

        this method provides the first option to access sensor data. this sensor subscribes on the model which executes the _data_callback if there is an update. the new data is updated to _data. when the user executes get_data(), it returns all data and clears the list, so that the users does not get the same data twice.

        Returns:
            List[T]: a list of data of type T
        """
        current_data = []

        while not self._data.empty():
            current_data.append(self._data.get())
        
        #first, i just made a copy of the list, cleared the ist and returned the data for the user. but i suspected race conditions in the time the data is transfered to the new list and before clearing the data from the _data list. if there was new data from the callback, we would accidently delete it, not knowing that it was there. but i am not sure if the event loop of python works like this. now we use a queue that is popped as long as it is not empty. safe not to lose data.

        return current_data
    
    def subscribe(self, callback: Callable[[T], None]) -> None:
        """
        subscribe to the sensor data that is updated when there is new data

        this methods registers a callback function from the user which is called when there is a sensor data update.

        Args:
            callback (Callable[[T], None]): a callback function which has the parameter of type T
        """
        if not callable(callback):
            raise TypeError(CERROR_MESSAGES.TYPE_MUST_BE_CALLABLE)

        try:
            self._callback_functions.append(callback)
        except:
            self._callback_functions = [callback]

    def _notify_callback_functions(self, data: T) -> None:
        """
        this function calls all callback functions when there is a data update in the model class

        this is the function which calls the callback function that is passed in subscribe()
        
        Args:
            data (T): a data point from type T
        """
        for callback in self._callback_functions:
            callback(data)

    def _data_callback(self, mayako_data: MayakoData) -> None:
        """
        this function is called when the model class has a new data point. As the get_sensor_data method from model returns a Dict, we also need to create an instance of the with this class associated model class. it updates the _data list and notifies all callback functions.

        Args:
            mayako_data (MayakoData): the model class with the data
        """
        data = mayako_data.get_sensor_data(self._mc_identity, self._identity)

        for datapoint in data:
            self._data.put(self._sensor_class_type.from_dict(datapoint))

        self._notify_callback_functions(data)

    def _subscribe_to_data(self) -> None:
        """this method subscribe the sensor to model data with typ associated in the event key"""
        self._model.add_sensor_to_data_list(self._mc_identity, self._identity)
        self._model.subscribe(self._sensor_data_callback_identity, self._data_callback)

    def define_capabilities(self, enable: bool = True, sample_rate: int = 10, data_on_state_change: bool = False) -> None:
        """
        this function lets the user change the capabilities of this sensor

        first, we check if there is a capabiltity that matches the identtiy of the microcontroller. then we create a new sensor capability object which

        Sources:
            K Yu (2016) Sampling interval and sampling rate/frequency - YouTube. Retrieved September 05, 2024, from https://www.youtube.com/watch?v=_iF-QNrZCU4&t=317s
            https://youtu.be/_iF-QNrZCU4?si=4WGSlzL2vugy0uwA

        Args:
            enable (bool): enables/disables the sensor in the record
            sample_rate (int): this is the times per second a data point is read from the microcontroller. check the video under Sources if the relation between sample rate and interval is not clear.
            data_on_state_change (bool): if True, the newly read data point on the microcontroller gets checked if it matches with the previous data point. if it does, the new data point is droped. no data point is sent from the microcontroller.
        """
        old_capas = self._check_capabilities(sensor_identity=self._identity)
        
        new_capas = SensorCapabilities(identity=self._identity, sample_rate=sample_rate, data_on_state_change=data_on_state_change, enable=enable)

        if not self._compare_sensor_capabilities(old_capas=old_capas, new_capas=new_capas):
            #we dont need to update the new capability because unlike with microcapabilities we
            self._logger.debug("updating sensor capability")
            self._model.update_sensor_capability(self._mc_identity, new_capas)
        else:
            self._logger.debug("no update on sensor capability")

    def _compare_sensor_capabilities(self, old_capas: SensorCapabilities, new_capas: SensorCapabilities) -> bool:
        """compares the sensor capabilities"""
        return (
            old_capas.enable == new_capas.enable and
            old_capas.sample_rate == new_capas.sample_rate and
            old_capas.data_on_state_change == new_capas.data_on_state_change
        )

    def _check_capabilities(self, sensor_identity: str) -> SensorCapabilities:
        """
        checks if there is a capability associated with the sensor identity
        
        Args:
            sensor_identity (str): identity of the sensor
        """
        capas = self._model.get_sensor_capability_by_identity(mc_identity=self._mc_identity, sensor_identity=sensor_identity)
        if not capas:
            raise Exception(f"the sensor with the provided identity {sensor_identity} does not exist in {CCLIENT.CONFIG_FILE_NAME}.")
        
        return capas

    def get_capabilities(self) -> SensorCapabilities:
        """returns the capabilities of the sensor"""
        return self._model.get_sensor_capability_by_identity(self._identity)