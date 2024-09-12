##
#
# File:    CreateRWTreeTest.py
# Author:  E. Peisach
# Date:    21-Dec-2019
# Version: 0.001
##
"""
Test cases for copying configurations

"""
__docformat__ = "restructuredtext en"
__author__ = "Ezra Peisach"
__email__ = "peisach@rcsb.rutgers.edu"
__license__ = "Creative Commons Attribution 3.0 Unported"
__version__ = "V0.01"

import os
import platform
import unittest
import shutil
from wwpdb.utils.testing.CreateRWTree import CreateRWTree


class CreateRWTreeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.__here = os.path.abspath(os.path.dirname(__file__))
        TESTOUTPUT = os.path.join(cls.__here, "test-output", platform.python_version(), "copytest")
        cls.__testout = TESTOUTPUT
        if os.path.exists(cls.__testout):
            shutil.rmtree(cls.__testout)

    def setUp(self):
        TOPDIR = os.path.dirname(os.path.dirname(os.path.dirname(self.__here)))
        if not os.path.exists(self.__testout):
            os.makedirs(self.__testout)

        mockTopPath = os.path.join(TOPDIR, "wwpdb", "mock-data")
        self.__crw = CreateRWTree(mockTopPath, self.__testout)

    def testCopySiteConfig(self):
        """Tests creation site-config"""
        self.__crw.createtree(["site-config"])
        self.assertTrue(os.path.exists(os.path.join(self.__testout, "site-config")))

    def testCopyActionData(self):
        """Test creation of actiondata.xml"""
        self.__crw.createtree(["actiondata"])
        self.assertTrue(os.path.exists(os.path.join(self.__testout, "da_top", "resources_ro", "actionData.xml")))

    def testCopyMultiData(self):
        """Test creation of multiple items"""
        dstdir = os.path.join(self.__testout, "da_top", "webapps")
        if os.path.exists(dstdir):
            shutil.rmtree(dstdir)
        self.__crw.createtree(["depuiresources", "emdresources", "wsresources", ["webapps", "msgmodule"]])
        self.assertTrue(os.path.exists(os.path.join(self.__testout, "da_top", "resources_ro", "depui")))
        self.assertTrue(os.path.exists(os.path.join(self.__testout, "da_top", "resources_ro", "emd")))
        self.assertTrue(os.path.exists(os.path.join(self.__testout, "da_top", "resources_ro", "content_ws")))
        self.assertTrue(os.path.exists(os.path.join(self.__testout, "da_top", "webapps", "htdocs", "msgmodule")))
        self.assertTrue(os.path.exists(os.path.join(self.__testout, "da_top", "webapps", "version.json")))

    def testCopyVersionOnly(self):
        """Test creation of version.json webapps"""
        dstdir = os.path.join(self.__testout, "da_top", "webapps")
        if os.path.exists(dstdir):
            shutil.rmtree(dstdir)
        self.__crw.createtree(["webapps"])
        self.assertFalse(os.path.exists(os.path.join(dstdir, "htdocs", "msgmodule")))
        self.assertTrue(os.path.exists(os.path.join(dstdir, "version.json")))

    def testCopyArchiveData(self):
        """Test creation of archive data"""
        self.__crw.createtree([["archive", "D_000001"]])
        self.assertTrue(os.path.exists(os.path.join(self.__testout, "da_top", "data", "archive", "D_000001")))

    def testCopyUnknown(self):
        """Test creation to log error"""
        self.__crw.createtree(["nothing"])


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
