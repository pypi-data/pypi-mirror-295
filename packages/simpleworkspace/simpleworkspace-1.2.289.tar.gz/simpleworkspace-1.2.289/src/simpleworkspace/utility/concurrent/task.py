import threading as _threading
from simpleworkspace.utility.time import StopWatch as _StopWatch
from simpleworkspace.types.time import TimeSpan as _TimeSpan
import abc as _abc

class Task:
    def __init__(self, action, *args, **kwargs):
        """
        :param action: the callback to run in the new thread
        :param *args: supplies positional arguments to the callback
        :param *kwargs: supplies default arguments to the callback
        """
        self.Daemon = False
        '''When task is marked as daemon, the task will automatically be terminated when main thread exits'''
        self.StopWatch = _StopWatch()
        self.Exception:Exception|None = None

        self._action = action
        self._args = args
        self._kwargs = kwargs
        self._thread = _threading.Thread(target=self._run)
        self._is_completed = False
        self._is_running = False
        self._result = None

    @property
    def IsRunning(self):
        return self._is_running
    
    @property
    def IsCompleted(self):
        return self._is_completed
    
    @property
    def _WasStarted(self):
        return self.IsRunning or self.IsCompleted
    
    def _run(self):
        self.StopWatch.Start()
        try:
            self._result = self._action(*self._args, **self._kwargs)
        except Exception as e:
            self.Exception = e
        finally:
            self.StopWatch.Stop()
            self._is_running = False
            self._is_completed = True

    def Start(self):
        if self._WasStarted:
            return
        self._is_running = True
        self._thread.daemon = self.Daemon
        self._thread.start()

    def Result(self, timeout:_TimeSpan=None):
        """awaits the results of the task

        :param timeout: awaits for a given amount of time, throws RuntimeError if not finished
        """
        if not(self._WasStarted):
            raise RuntimeError("Task has not been started yet...")
        if not self.IsCompleted:
            self.Wait(timeout)
            if not self.IsCompleted:
                raise TimeoutError("Task did not finish before timeout")
        if self.Exception:
            raise self.Exception
        return self._result

    def Wait(self, timeout:_TimeSpan=None):
        """
        Wait for the thread to finish

        :param timeout: blocks for a given amount of time, before resuming
        """
        if not(self._WasStarted):
            raise RuntimeError("Task has not been started yet...")
        if(timeout):
            timeout = timeout.TotalSeconds
        self._thread.join(timeout)


class ITask(Task, _abc.ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(self._Action, *args, **kwargs)

    @_abc.abstractmethod
    def _Action(task, *args, **kwargs):
        '''Child class implements task here'''
 
class ITaskCancellable(Task, _abc.ABC):
    '''
    Example::

        class ExampleTask(ITaskCancellable):
            def _Action(task):
                while not task.IsCancelled:
                    #do work...
                    task._cancellationToken.wait(1) #sleep 1 second

        task = ExampleTask()
        task.Start()
    '''
    def __init__(self, *args, **kwargs):
        self._cancellationToken = _threading.Event()
        super().__init__(self._Action, *args, **kwargs)

    @_abc.abstractmethod
    def _Action(task, *args, **kwargs):
        '''Child class implements task here, provides implementer with cancellationtoken'''

    @property
    def IsCancelled(self):
        return self._cancellationToken.is_set()

    def Cancel(self):
        self._cancellationToken.set()

    def Start(self):
        if(self.IsCancelled):
            return
        return super().Start()