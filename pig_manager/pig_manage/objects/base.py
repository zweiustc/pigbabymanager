from oslo_versionedobjects import base as ovoo_base

class BaseObject(ovoo_base.VersionedObject,
                 ovoo_base.VersionedObjectDictCompat):
    """Base class and object factory.

    This forms the base of all objects that can be remoted or instantiated
    via RPC. Simply defining a class that inherits from this base class
    will make it remotely instantiatable. Objects should implement the
    necessary "get" classmethod routines as well as "save" object methods
    as appropriate.
    """

    OBJ_SERIAL_NAMESPACE = 'kingcloudos_object'
    OBJ_PROJECT_NAMESPACE = 'kingcloudos'
    def as_dict(self):
        return {k: getattr(self, k)
                for k in self.fields
                if self.obj_attr_is_set(k)}


class ObjectRegistry(ovoo_base.VersionedObjectRegistry):
    pass
