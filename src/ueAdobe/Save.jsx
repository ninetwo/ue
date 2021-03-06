﻿#include "Core.jsx"

Save();

var win;
var elements, elclasses;
var ueproj, uegrp, ueasst, ueclass, uetype, uename = null;

function Save()
{
  if (BridgeTalk.appName == "photoshop")
  {
    elclasses = ["ps", "bg"];
  }
  else if (BridgeTalk.appName == "aftereffects")
  {
    elclasses = ["ae"];
  }

  win = new Window("dialog", "ueSave", [100,100,670,350]);

  win.assetPanel = win.add("panel", [10,10,560,70], "Asset");
  win.elementPanel = win.add("panel", [10,80,560,210], "Element");

  win.assetPanel.add("StaticText", [10,20,60,37], "Project");
  win.assetPanel.add("StaticText", [190,20,240,37], "Group");
  win.assetPanel.add("StaticText", [360,20,410,37], "Asset");
  win.assetPanel.projectList = win.assetPanel.add("DropDownList", [70,20,176,35]);
  win.assetPanel.groupList = win.assetPanel.add("DropDownList", [240,20,346,35]);
  win.assetPanel.assetList = win.assetPanel.add("DropDownList", [410,20,516,35]);

  win.elementPanel.add("StaticText", [10,20,60,37], "Class");
  win.elementPanel.add("StaticText", [10,50,60,67], "Type");
  win.elementPanel.add("StaticText", [10,80,60,97], "Name");
  win.elementPanel.classList = win.elementPanel.add("DropDownList", [70,20,190,35]);
  win.elementPanel.typeList = win.elementPanel.add("DropDownList", [70,50,190,65]);
  win.elementPanel.nameList = win.elementPanel.add("DropDownList", [70,80,190,95]);
  win.elementPanel.typeBox = win.elementPanel.add("EditText", [200,50,370,66]);
  win.elementPanel.nameBox = win.elementPanel.add("EditText", [200,80,370,96]);
	
  win.okButton = win.add("Button", [450,220,550,240], "OK");
  win.cancelButton = win.add("Button", [340,220,440,240], "Cancel");
  
  var projects = getProjectsList();
  for(var p = 0; p < projects.length; p++)
  {
    win.assetPanel.projectList.add("item", projects[p]);
  }
  win.assetPanel.projectList.items[0].selected = true;
  ueproj = win.assetPanel.projectList.selection.text;

  var groups = getGroupsList(ueproj);
  for(var g = 0; g < groups.length; g++)
  {
    win.assetPanel.groupList.add("item", groups[g]);
  }
  win.assetPanel.groupList.items[0].selected = true;
  uegrp = win.assetPanel.groupList.selection.text;
  
  var assets = getAssetsList(ueproj, uegrp);
  for(var a = 0; a < assets.length; a++)
  {
    win.assetPanel.assetList.add("item", assets[a]);
  }
  win.assetPanel.assetList.items[0].selected = true;
  ueasst = win.assetPanel.assetList.selection.text;

  elements = getElements(ueproj, uegrp, ueasst);

  for(var c = 0; c < elclasses.length; c++)
  {
    win.elementPanel.classList.add("item", elclasses[c]);
  }

  win.elementPanel.classList.items[0].selected = true;
  ueclass = win.elementPanel.classList.selection.text;

  if (ueclass in elements)
  {
  for(e in elements[ueclass])
  {
    win.elementPanel.typeList.add("item", e);
  }
  win.elementPanel.typeList.items[0].selected = true;
  uetype = win.elementPanel.typeList.selection.text;

  if (uetype in elements[ueclass])
  {
    for(e in elements[ueclass][uetype])
    {
      win.elementPanel.nameList.add("item", e);
    }
    win.elementPanel.nameList.items[0].selected = true;
    uename = win.elementPanel.nameList.selection.text;
  }
  }

  win.assetPanel.projectList.onChange = setGroups;
  win.assetPanel.groupList.onChange = setAssets;
  win.assetPanel.assetList.onChange = setElements;
  win.elementPanel.classList.onChange = setTypes;
  win.elementPanel.typeList.onChange = setNames;
  win.elementPanel.nameList.onChange = setName;
  win.elementPanel.typeBox.onChange = setNewType;
  win.elementPanel.nameBox.onChange = setNewName;
  win.okButton.onClick = saveFile;
  
  win.show();
}


function saveFile() {
  if (getElement(ueproj, uegrp, ueasst, ueclass, uetype, uename) == null)
  {
    createElement(ueproj, uegrp, ueasst, ueclass, uetype, uename);
  }
  createVersion(ueproj, uegrp, ueasst, ueclass, uetype, uename);

  var uevers = getVersions(ueproj, uegrp, ueasst, ueclass, uetype, uename).length;
  var version = getVersion(ueproj, uegrp, ueasst, ueclass, uetype, uename, uevers);

  var path = version["path"];
  var file = version["file_name"];
  var ext = getExtension(ueclass);

  var f = new File(parsePath(path)+"/"+file+"."+ext);

  if (BridgeTalk.appName == "photoshop")
  {
    var doc = activeDocument;
    var saveOptions = new PhotoshopSaveOptions();

    doc.info.title = file;

    doc.saveAs(f, saveOptions, false, Extension.LOWERCASE);
  }
  else if (BridgeTalk.appName == "aftereffects")
  {
    var doc = app.project;

    doc.save(f);
  }

  win.close();
}


function setGroups() {
  ueproj = win.assetPanel.projectList.selection.text;
  var groups = getGroupsList(ueproj);
  win.assetPanel.groupList.removeAll();
  for(var g = 0; g < groups.length; g++)
  {
    win.assetPanel.groupList.add("item", groups[g]);
  }
  if (groups.length > 0)
  {
    win.assetPanel.groupList.items[0].selected = true;
    uegrp = win.assetPanel.groupList.selection.text;
  }
  else
  {
    uegrp = null;
    ueasst = null;
    ueclass = null;
    uetype = null;
    uename = null;
    win.assetPanel.assetList.removeAll();
    win.elementPanel.classList.removeAll();
    win.elementPanel.typeList.removeAll();
    win.elementPanel.nameList.removeAll();
  }
}

function setAssets() {
  if (win.assetPanel.groupList.selection != null)
  {
    uegrp = win.assetPanel.groupList.selection.text;
    var assets = getAssetsList(ueproj, uegrp);
    win.assetPanel.assetList.removeAll();
    for(var a = 0; a < assets.length; a++)
    {
      win.assetPanel.assetList.add("item", assets[a]);
    }
    if (assets.length > 0)
    {
      win.assetPanel.assetList.items[0].selected = true;
      ueasst = win.assetPanel.assetList.selection.text;
    }
    else
    {
      ueasst = null;
      ueclass = null;
      uetype = null;
      uename = null;
      win.elementPanel.classList.removeAll();
      win.elementPanel.typeList.removeAll();
      win.elementPanel.nameList.removeAll();
    }
  }
}

function setElements() {
  if (win.assetPanel.assetList.selection != null)
  {
    ueasst = win.assetPanel.assetList.selection.text;
    elements = getElements(ueproj, uegrp, ueasst);
    win.elementPanel.classList.removeAll();
    for(var c = 0; c < elclasses.length; c++)
    {
      win.elementPanel.classList.add("item", elclasses[c]);
    }
    win.elementPanel.classList.items[0].selected = true;
    ueclass = win.elementPanel.classList.selection.text;
  }
}

function setNewType() {
  uetype = win.elementPanel.typeBox.text;
}

function setNewName() {
  uename = win.elementPanel.nameBox.text;
}

function setTypes() {
  if (win.elementPanel.classList.selection != null)
  {
    ueclass = win.elementPanel.classList.selection.text;
    win.elementPanel.typeList.removeAll();
	if (ueclass in elements)
    {
      for(e in elements[ueclass])
      {
        win.elementPanel.typeList.add("item", e);
      }
      win.elementPanel.typeList.items[0].selected = true;
      uetype = win.elementPanel.typeList.selection.text;
    }
  }
}

function setNames() {
  if (win.elementPanel.typeList.selection != null)
  {
    uetype = win.elementPanel.typeList.selection.text;
    win.elementPanel.nameList.removeAll();
    for(e in elements[ueclass][uetype])
    {
      win.elementPanel.nameList.add("item", e);
    }
    win.elementPanel.nameList.items[0].selected = true;
    uename = win.elementPanel.nameList.selection.text;
  }
}

function setName() {
  if (win.elementPanel.nameList.selection != null)
  {
    uename = win.elementPanel.nameList.selection.text;
  }
}

