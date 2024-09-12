# -*- coding: utf-8 -*-
__all__ = ["QuackamollieModelManagerRegistry"]
__author__ = "QuacktorAI"
__copyright__ = "Copyright 2024, Forge of Absurd Ducks"
__credits__ = ["QuacktorAI"]

from importlib.metadata import entry_points
from typing import Dict, Optional, Type

from quackamollie.core.meta.model_manager.meta_quackamollie_model_manager import MetaQuackamollieModelManager
from quackamollie.core.utils.singleton import Singleton


class QuackamollieModelManagerRegistryBaseClass:
    """ A registry of MetaQuackamollieModelManager listing them using a dedicated entrypoint """

    MODEL_MANAGER_ENTRYPOINT_GROUP: str = "quackamollie.model_manager"

    def __init__(self):
        self._model_managers: Optional[Dict[str, Type[MetaQuackamollieModelManager]]] = None
        self._model_managers_by_class_name: Optional[Dict[str, Type[MetaQuackamollieModelManager]]] = None
        self._class_name_to_entrypoint_name: Optional[Dict[str, str]] = None

    def load_model_managers(self):
        """ Load MetaQuackamollieModelManager registered as entrypoints in the group MODEL_MANAGER_ENTRYPOINT_GROUP """
        self._model_managers = {}
        self._model_managers_by_class_name = {}
        self._class_name_to_entrypoint_name = {}

        for script in entry_points(group=self.MODEL_MANAGER_ENTRYPOINT_GROUP):
            try:
                model_manager_class = script.load()
            except Exception as error:
                self._model_managers = None
                self._model_managers_by_class_name = None
                self._class_name_to_entrypoint_name = None
                raise AttributeError(f"Error loading QuackamollieModelManager from entrypoint"
                                     f" with name '{script.name}' in group '{self.MODEL_MANAGER_ENTRYPOINT_GROUP}',"
                                     f" with exception:\n{error}")

            if issubclass(model_manager_class, MetaQuackamollieModelManager):
                self._model_managers[script.name] = model_manager_class
                self._model_managers_by_class_name[model_manager_class.__name__] = model_manager_class
                self._class_name_to_entrypoint_name[model_manager_class.__name__] = script.name
            else:
                self._model_managers = None
                self._model_managers_by_class_name = None
                self._class_name_to_entrypoint_name = None
                raise AttributeError(f"Error loaded class '{model_manager_class.__name__}', from entrypoint"
                                     f" with name '{script.name}' in group '{self.MODEL_MANAGER_ENTRYPOINT_GROUP}',"
                                     f" doesn't inherit from MetaQuackamollieModelManager.")

    @property
    def model_managers(self) -> Dict[str, Type[MetaQuackamollieModelManager]]:
        """ Property to get the model managers loaded from entrypoints using the method `load_model_managers`

            :return: A dictionary with the entrypoint names as keys and as values the loaded
                     subclasses of MetaQuackamollieModelManager
            :rtype: Dict[str, Type[MetaQuackamollieModelManager]]
        """
        return self._model_managers

    @property
    def model_managers_by_class_name(self) -> Dict[str, Type[MetaQuackamollieModelManager]]:
        """ Property to get the model managers loaded from entrypoints using the method `load_model_managers`,
            indexed by class name

            :return: A dictionary with the class names as keys and as values the loaded
                     subclasses of MetaQuackamollieModelManager
            :rtype: Dict[str, Type[MetaQuackamollieModelManager]]
        """
        return self._model_managers_by_class_name

    @property
    def class_name_to_entrypoint_name(self) -> Dict[str, str]:
        """ Property to get the model manager entrypoint name from it class name

            :return: A dictionary with the class names as keys and as values the entrypoint names
            :rtype: Dict[str, str]
        """
        return self._class_name_to_entrypoint_name


class QuackamollieModelManagerRegistry(QuackamollieModelManagerRegistryBaseClass, metaclass=Singleton):
    """ Singleton that stores the model manager registry to retrieve model managers loaded from entrypoints"""
    pass
