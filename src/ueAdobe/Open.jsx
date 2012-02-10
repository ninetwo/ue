#include "Core.jsx"

Open();

var win;
var elements, elclasses;
var ueproj, uegrp, ueasst, ueclass, uetype, uename, uevers = null;

function Open()
{
  if (BridgeTalk.appName == "photoshop")
  {
    elclasses = ["ps"];
  }
  else if (BridgeTalk.appName == "aftereffects")
  {
    elclasses = ["ae"];
  }

  win = new Window("dialog", "ueOpen", [100,100,670,500]);

  win.assetPanel = win.add("panel", [10,10,560,70], "Asset");
  win.elementPanel = win.add("panel", [10,80,560,360], "Element");

  win.assetPanel.add("StaticText", [10,20,60,37], "Project");
  win.assetPanel.add("StaticText", [190,20,240,37], "Group");
  win.assetPanel.add("StaticText", [360,20,410,37], "Asset");
  win.assetPanel.projectList = win.assetPanel.add("DropDownList", [70,20,176,35]);
  win.assetPanel.groupList = win.assetPanel.add("DropDownList", [240,20,346,35]);
  win.assetPanel.assetList = win.assetPanel.add("DropDownList", [410,20,516,35]);

  win.elementPanel.add("StaticText", [10,10,111,27], "Class");
  win.elementPanel.add("StaticText", [10,140,111,157], "Type");
  win.elementPanel.add("StaticText", [190,10,291,27], "Name");
  win.elementPanel.add("StaticText", [370,10,471,27], "Version");
  win.elementPanel.classList = win.elementPanel.add("ListBox", [10,30,180,130]);
  win.elementPanel.typeList = win.elementPanel.add("ListBox", [10,160,180,260]);
  win.elementPanel.nameList = win.elementPanel.add("ListBox", [190,30,360,260]);
  win.elementPanel.versList = win.elementPanel.add("ListBox", [370,30,540,260]);

  win.okButton = win.add("Button", [450,370,550,390], "OK");
  win.cancelButton = win.add("Button", [340,370,440,390], "Cancel");
  
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

  if (ueclass in elements)
  {
    win.elementPanel.classList.items[0].selected = true;
    ueclass = win.elementPanel.classList.selection.text;

    for(e in elements[ueclass])
    {
      win.elementPanel.typeList.add("item", e);
    }
    win.elementPanel.typeList.items[0].selected = true;
    uetype = win.elementPanel.typeList.selection.text;

    if (win.elementPanel.typeList.selection != null)
    {
      for(e in elements[ueclass][uetype])
      {
        win.elementPanel.nameList.add("item", e);
      }
      win.elementPanel.nameList.items[0].selected = true;
      uename = win.elementPanel.nameList.selection.text;

      var versions = getVersions(ueproj, uegrp, ueasst, ueclass, uetype, uename);

      for(var v = 0; v < versions.length; v++)
      {
        win.elementPanel.versList.add("item", versions[v]["version"]);
      }
      win.elementPanel.versList.items[0].selected = true;
      uevers = win.elementPanel.versList.selection.text;
    }
  }

  win.assetPanel.projectList.onChange = setGroups;
  win.assetPanel.groupList.onChange = setAssets;
  win.assetPanel.assetList.onChange = setElements;
  win.elementPanel.classList.onChange = setTypes;
  win.elementPanel.typeList.onChange = setNames;
  win.elementPanel.nameList.onChange = setVers;
  win.elementPanel.versList.onChange = selectVers;
  win.okButton.onClick = openFile;
  
  win.show();
}


function openFile() {
  var path = getVersionPath(ueproj, uegrp, ueasst, ueclass, uetype, uename, uevers);
  var file = getElementName(ueproj, uegrp, ueasst, ueclass, uetype, uename, uevers);

  if (BridgeTalk.appName == "photoshop")
  {
    var f = new File(parsePath(path)+"/"+file+".psd");
    open(f);
  }
  else if (BridgeTalk.appName == "aftereffects")
  {
    var f = new File(parsePath(path)+"/"+file+".aep");
    app.open(f);
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
    uevers = null;
    win.assetPanel.assetList.removeAll();
    win.elementPanel.classList.removeAll();
    win.elementPanel.typeList.removeAll();
    win.elementPanel.nameList.removeAll();
    win.elementPanel.versList.removeAll();
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
      uevers = null;
      win.elementPanel.classList.removeAll();
      win.elementPanel.typeList.removeAll();
      win.elementPanel.nameList.removeAll();
      win.elementPanel.versList.removeAll();
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

function setVers() {
  if (win.elementPanel.nameList.selection != null)
  {
    uename = win.elementPanel.nameList.selection.text;
    var versions = getVersions(ueproj, uegrp, ueasst, ueclass, uetype, uename);
    win.elementPanel.versList.removeAll();
    for (var v = 0; v < versions.length; v++)
    {
      win.elementPanel.versList.add("item", versions[v]["version"]);
    }
    if (versions.length > 0)
    {
      win.elementPanel.versList.items[0].selected = true;
      uevers = win.elementPanel.versList.selection.text;
    }
  }
}

function selectVers() {
  if (win.elementPanel.versList.selection != null)
  {
    uevers = win.elementPanel.versList.selection.text;
  }
}

