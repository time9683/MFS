import pytest
from classes_functions import *

def test_file_init():
    file = File("test_file", 100, "2022-01-01", "2022-01-01", ".txt", "This is a test file")
    assert file.name == "test_file"
    assert file.size == 100
    assert file.modifyDate == "2022-01-01"
    assert file.creationDate == "2022-01-01"
    assert file.extension == ".txt"
    assert file.content == "This is a test file"
    

def test_folder_init():
    folder = Folder("test_folder", "2022-01-01", "2022-01-01")
    assert folder.name == "test_folder"
    assert folder.modifyDate == "2022-01-01"
    assert folder.creationDate == "2022-01-01"    
    # test add files and folders here
    f1 = File("test_file", 100, "2022-01-01", "2022-01-01", ".txt", "This is a test file")
    f2 = File("test_file2", 20, "2022-01-05", "2022-01-01", ".txt", "This is a content for test") 
    folder.append(f1)
    folder.append(f2)
    print(folder.files)
    assert folder.files[0] == f1
    assert folder.files[1] == f2
    assert folder.size == 120
    folder2 = Folder("test_folder2", "2022-01-01", "2022-01-01")
    folder2.size = 200
    folder.append(folder2)
    assert folder.folders[0] == folder2
    assert folder.size == 320
    
    
    

def test_unit_init():
    unit = Unit("test_unit", 1000, "HDD")
    assert unit.name == "test_unit"
    assert unit.totalSize == 1000
    assert unit.type == "HDD"

    folder = Folder("test1", "2022-01-01", "2022-01-01")
    folder2 = Folder("test2", "2022-01-01", "2022-01-01")
    folder.size = 150
    folder2.size = 200
    unit.append(folder)
    unit.append(folder2)
    assert unit.folders[0] == folder
    assert unit.folders[1] == folder2
    assert unit.freeSize ==  650



def test_size_sort():

    f1 = File("test_file", 100, "2022-01-01", "2022-01-01", ".txt", "This is a test file")
    f2 = File("test_file2", 20, "2022-01-05", "2022-01-01", ".txt", "This is a content for test")
    f3 = File("test_file3", 50, "2022-01-05", "2022-01-01", ".txt", "This is a content for test")
    f4 = File("test_file4", 10, "2022-01-05", "2022-01-01", ".txt", "This is a content for test")
    files = [f1, f2, f3, f4]
    files = size_sort(files,"desc")
    assert files == [f1, f3, f2, f4]
    files = size_sort(files,"asc")
    assert files == [f4, f2, f3, f1]
    
def test_value_sort():

    f1 = File("test_file", 100, "2022-01-01", "2022-01-01", ".txt", "This is a test file")
    f5 = File("test_file", 120, "2022-01-01", "2022-01-01", ".txt", "This is a test file")
    f2 = File("test_file2", 20, "2022-01-05", "2022-01-01", ".txt", "This is a content for test")
    f3 = File("test_file3", 50, "2022-01-05", "2022-01-01", ".txt", "This is a content for test")
    f4 = File("test_file4", 10, "2022-01-05", "2022-01-01", ".txt", "This is a content for test")
    files = [f1, f2, f3, f4, f5]
    f_up = value_sort(files,50,">","desc")
    assert f_up == [f5,f1]
    f_down = value_sort(files,50,"<","desc")
    assert f_down == [f2, f4]
    f_equal = value_sort(files,50,"=","desc")
    assert f_equal == [f3]
    
def test_last_update_sort():

    f1 = File("test_file", 100, "2022-01-01", "2024-02-05", ".txt", "This is a test file")
    f2 = File("test_file2", 20, "2022-01-05", "2023-05-01", ".txt", "This is a content for test")
    f3 = File("test_file3", 50, "2022-01-05", "2021-07-01", ".txt", "This is a content for test")    
    f4 = File("test_file4", 10, "2022-01-05", "2022-01-01", ".txt", "This is a content for test")
    files = [f1, f2, f3, f4]
    
    f_up = last_update_sort(files,"desc")
    assert f_up == [f1,f2,f4,f3]
    f_down = last_update_sort(files,"asc")
    assert f_down == [f3,f4,f2,f1]    
    
    
def test_creation_sort():

    f1 = File("test_file", 100, "2024-01-02", "2024-02-05", ".txt", "This is a test file")
    f2 = File("test_file2", 20, "2023-02-03", "2023-05-01", ".txt", "This is a content for test")
    f3 = File("test_file3", 50, "2018-03-02", "2021-07-01", ".txt", "This is a content for test")    
    f4 = File("test_file4", 10, "2021-02-07", "2022-01-01", ".txt", "This is a content for test")
    files = [f1, f2, f3, f4]
    
    f_up = creation_sort(files,"desc")
    assert f_up == [f1,f2,f4,f3]
    f_down = creation_sort(files,"asc")
    assert f_down == [f3,f4,f2,f1]