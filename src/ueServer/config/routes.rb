UeServer::Application.routes.draw do
  match "/projects"                => "projects#index",   :as => :projects, :via => :get
  match "/projects"                => "projects#create",  :as => :project,  :via => :post
  match "/projects"                => "projects#update",  :as => :project,  :via => :put
  match "/projects"                => "projects#destroy", :as => :project,  :via => :destroy
  match "/projects/:proj"          => "projects#show",    :as => :project

  match "/groups/:proj"            => "groups#index",   :as => :groups, :via => :get
  match "/groups/:proj"            => "groups#create",  :as => :group,  :via => :post
  match "/groups/:proj"            => "groups#update",  :as => :group,  :via => :put
  match "/groups/:proj"            => "groups#destroy", :as => :group,  :via => :destroy
  match "/groups/:proj/:grp"       => "groups#show",    :as => :group

  match "/assets/:proj/:grp"       => "assets#index",   :as => :assets, :via => :get
  match "/assets/:proj/:grp"       => "assets#create",  :as => :asset,  :via => :post
  match "/assets/:proj/:grp"       => "assets#update",  :as => :asset,  :via => :put
  match "/assets/:proj/:grp"       => "assets#destroy", :as => :asset,  :via => :destroy
  match "/assets/:proj/:grp/:asst" => "assets#show",    :as => :asset

  match "/elements/:proj/:grp/:asst"                          => "elements#index",   :as => :elements
  match "/elements/:proj/:grp/:asst/:elclass/:eltype/:elname" => "elements#show",    :as => :element,  :via => :get
  match "/elements/:proj/:grp/:asst/:elclass/:eltype/:elname" => "elements#create",  :as => :element,  :via => :post
  match "/elements/:proj/:grp/:asst/:elclass/:eltype/:elname" => "elements#update",  :as => :element,  :via => :put
  match "/elements/:proj/:grp/:asst/:elclass/:eltype/:elname" => "elements#destroy", :as => :element,  :via => :destroy

  match "/versions/:proj/:grp/:asst/:elclass/:eltype/:elname" => "elements#create_version", :as => :version, :via => :post

  root :to => 'projects#index'
end
