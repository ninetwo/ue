﻿function getProjects()
{
  var url = "192.168.0.5:3000";
  var path = "/projects.json";
  var conn = new Socket;
  if (conn.open (url)) {
    conn.write ("GET "+path+" HTTP/1.0\n\n");
    var reply = conn.read(9999999999);
	reply = reply.substr(reply.indexOf("\n\n")+2);
    conn.close();
  }
  return eval(reply);
}

function getProjectsList()
{
  var projects = getProjects();
  var projectsList = [];
  for (var p = 0; p < projects.length; p++)
  {
    projectsList[p] = projects[p]["name"];
  }
  return projectsList;
}

function getGroups(proj)
{
  var url = "192.168.0.5:3000";
  var path = "/groups/"+proj+".json";
  var conn = new Socket;
  if (conn.open (url)) {
    conn.write ("GET "+path+" HTTP/1.0\n\n");
    var reply = conn.read(9999999999);
	reply = reply.substr(reply.indexOf("\n\n")+2);
    conn.close();
  }
  return eval(reply);
}

function getGroupsList(proj)
{
  var groups = getGroups(proj);
  var groupsList = [];
  for (var g = 0; g < groups.length; g++)
  {
    groupsList[g] = groups[g]["name"];
  }
  return groupsList;
}

function getAsset(proj, grp, asst)
{
  var url = "192.168.0.5:3000";
  var path = "/assets/"+proj+"/"+grp+"/"+asst+".json";
  var conn = new Socket;
  if (conn.open (url)) {
    conn.write ("GET "+path+" HTTP/1.0\n\n");
    var reply = conn.read(9999999999);
	reply = reply.substr(reply.indexOf("\n\n")+2);
    conn.close();
  }
  return eval("("+reply+")");
}

function getAssets(proj, grp)
{
  var url = "192.168.0.5:3000";
  var path = "/assets/"+proj+"/"+grp+".json";
  var conn = new Socket;
  if (conn.open (url)) {
    conn.write ("GET "+path+" HTTP/1.0\n\n");
    var reply = conn.read(9999999999);
	reply = reply.substr(reply.indexOf("\n\n")+2);
    conn.close();
  }
  return eval(reply);
}

function getAssetsList(proj, grp)
{
  var assets = getAssets(proj, grp);
  var assetsList = [];
  for (var a = 0; a < assets.length; a++)
  {
    assetsList[a] = assets[a]["name"];
  }
  return assetsList;
}

function getElement(proj, grp, asst, elclass, eltype, elname)
{
  var url = "192.168.0.5:3000";
  var path = "/elements/"+proj+"/"+grp+"/"+asst+"/"+elclass+"/"+eltype+"/"+elname+".json";
  var conn = new Socket;
  if (conn.open (url)) {
    conn.write ("GET "+path+" HTTP/1.0\n\n");
    var reply = conn.read(9999999999);
	reply = reply.substr(reply.indexOf("\n\n")+2);
    conn.close();
  }
  return eval("("+reply+")");
}

function getElements(proj, grp, asst)
{
  var url = "192.168.0.5:3000";
  var path = "/elements/"+proj+"/"+grp+"/"+asst+".json";
  var conn = new Socket;
  if (conn.open (url)) {
    conn.write ("GET "+path+" HTTP/1.0\n\n");
    var reply = conn.read(9999999999);
	reply = reply.substr(reply.indexOf("\n\n")+2);
    conn.close();
  }
  var e = {};
  var elementsDict = eval(reply);
  for (var i = 0; i < elementsDict.length; i++)
  {
    if (!(elementsDict[i]["elclass"] in e))
    {
      e[elementsDict[i]["elclass"]] = {};
    }
    if (!(elementsDict[i]["eltype"] in e[elementsDict[i]["elclass"]]))
    {
      e[elementsDict[i]["elclass"]][elementsDict[i]["eltype"]] = {};
    }
    if (!(elementsDict[i]["elname"] in e[elementsDict[i]["elclass"]][elementsDict[i]["eltype"]]))
    {
      e[elementsDict[i]["elclass"]][elementsDict[i]["eltype"]][elementsDict[i]["elname"]] = {};
    }
    e[elementsDict[i]["elclass"]][elementsDict[i]["eltype"]][elementsDict[i]["elname"]]["path"] = elementsDict[i]["path"];
  }
  return e;
}

function getVersions(proj, grp, asst, elclass, eltype, elname)
{
  var element = getElement(proj, grp, asst, elclass, eltype, elname);
  if (element == null)
  {
    element = {};
    element["versions"] = [];
  }
  return element["versions"];
}


function createElement(proj, grp, asst, elclass, eltype, elname) {
  var path = getElementPath(proj, grp, asst, elclass, eltype, elname);
  var element = "path="+path+"&created_by=thoms";
  var url = "192.168.0.5";
  var port = "3000";
  var path = "/elements/"+proj+"/"+grp+"/"+asst+"/"+elclass+"/"+eltype+"/"+elname+".json";
  var conn = new Socket;
  if (conn.open (url+":"+port)) {
    conn.write("POST "+path+" HTTP/1.0\r\n");
    conn.write("Host: "+url+"\r\n");
    conn.write("Content-Length: "+element.length+"\r\n");
    conn.write("Content-Type: application/x-www-form-urlencoded\r\n");
    conn.write("\r\n");
    conn.write(element);
    var reply = conn.read(9999999999);
	reply = reply.substr(reply.indexOf("\n\n")+2);
    conn.close();
  }
}

function createVersion(proj, grp, asst, elclass, eltype, elname) {
  var version = getVersions(proj, grp, asst, elclass, eltype, elname).length+1;
  var path = getVersionPath(proj, grp, asst, elclass, eltype, elname, version);
  var vers = "path="+path+"&version="+version+"&created_by=thoms";
  var url = "192.168.0.5";
  var port = "3000";
  var path = "/versions/"+proj+"/"+grp+"/"+asst+"/"+elclass+"/"+eltype+"/"+elname+".json";
  var conn = new Socket;
  if (conn.open (url+":"+port)) {
    conn.write("POST "+path+" HTTP/1.0\r\n");
    conn.write("Host: "+url+"\r\n");
    conn.write("Content-Length: "+vers.length+"\r\n");
    conn.write("Content-Type: application/x-www-form-urlencoded\r\n");
    conn.write("\r\n");
    conn.write(vers);
    var reply = conn.read(9999999999);
	reply = reply.substr(reply.indexOf("\n\n")+2);
    conn.close();
  }
}


function getElementPath(proj, grp, asst, elclass, eltype, elname) {
  var asset = getAsset(proj, grp, asst);
  return asset["path"]+"/"+eltype+"/"+elname;
}

function getVersionPath(proj, grp, asst, elclass, eltype, elname, vers) {
  var element = getElementPath(proj, grp, asst, elclass, eltype, elname);
  return element;
}

function getElementName(proj, grp, asst, elclass, eltype, elname, vers)
{
  return proj+"_"+grp+"_"+asst+"_"+eltype+"_"+elname+"_"+elclass+"_"+pad(vers);
}


function parsePath(path)
{
  // Mac
  return path.replace(/^\/work/, "/Volumes/work");
  // Windows
}

function pad(number)
{
  var str = "" + number;
  while (str.length < 4)
  {
    str = "0" + str;
  }
  return str;
}

