from oslo_versionedobjects import base as ovoo_base


remotable_classmethod = ovoo_base.remotable_classmethod
remotable = ovoo_base.remotable

class BaseObject(ovoo_base.VersionedObject,
                 ovoo_base.VersionedObjectDictCompat):
    """Base class and object factory.

    This forms the base of all objects that can be remoted or instantiated
    via RPC. Simply defining a class that inherits from this base class
    will make it remotely instantiatable. Objects should implement the
    necessary "get" classmethod routines as well as "save" object methods
    as appropriate.
    """

    OBJ_SERIAL_NAMESPACE = 'pig_manage_object'
    OBJ_PROJECT_NAMESPACE = 'pig_manage'
    def as_dict(self):
        return {k: getattr(self, k)
                for k in self.fields
                if self.obj_attr_is_set(k)}


class ObjectRegistry(ovoo_base.VersionedObjectRegistry):
    pass


class ObjectSerializer(ovoo_base.VersionedObjectSerializer):
    # Base class to use for object hydration
    OBJ_BASE_CLASS = BaseObject


class PageList(object):
    """A pageList class  contains total count and selected objects..
    """ 
    def __init__(self, objects, total):
        self._list = objects
        super(PageList, self).__init__()
        self.total = total

    def __getattr__(self, item):
        return getattr(self._list, item)

    def __iter__(self):
        """List iterator interface."""
        return iter(self._list)

    def __len__(self):
        """List length."""
        return len(self._list)

    def __contains__(self, value):
        """List membership test."""
        return value in self._list

    def __getitem__(self, index):
        """List index access."""
        return self._list.__getitem__(index)
