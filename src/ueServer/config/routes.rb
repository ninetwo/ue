UeServer::Application.routes.draw do
  match "/projects"                => "projects#index",   :as => :projects, :via => :get
  match "/projects"                => "projects#create",  :as => :project,  :via => :post
  match "/projects"                => "projects#update",  :as => :project,  :via => :put
  match "/projects/:proj"          => "projects#destroy", :as => :project,  :via => :delete
  match "/projects/:proj"          => "projects#show",    :as => :project

  match "/groups/:proj"            => "groups#index",   :as => :groups, :via => :get
  match "/groups/:proj"            => "groups#create",  :as => :group,  :via => :post
  match "/groups/:proj/:grp"       => "groups#update",  :as => :group,  :via => :put
  match "/groups/:proj/:grp"       => "groups#destroy", :as => :group,  :via => :delete
  match "/groups/:proj/:grp"       => "groups#show",    :as => :group

  match "/ueassets/:proj/:grp"       => "assets#index",   :as => :assets, :via => :get
  match "/ueassets/:proj/:grp"       => "assets#create",  :as => :asset,  :via => :post
  match "/ueassets/:proj/:grp/:asst" => "assets#update",  :as => :asset,  :via => :put
  match "/ueassets/:proj/:grp/:asst" => "assets#destroy", :as => :asset,  :via => :delete
  match "/ueassets/:proj/:grp/:asst" => "assets#show",    :as => :asset

  match "/elements/:proj/:grp/:asst"                          => "elements#index",   :as => :elements
  match "/elements/:proj/:grp/:asst/:elclass/:eltype/:elname" => "elements#show",    :as => :element,  :via => :get
  match "/elements/:proj/:grp/:asst/:elclass/:eltype/:elname" => "elements#create",  :as => :element,  :via => :post
  match "/elements/:proj/:grp/:asst/:elclass/:eltype/:elname" => "elements#update",  :as => :element,  :via => :put
  match "/elements/:proj/:grp/:asst/:elclass/:eltype/:elname" => "elements#destroy", :as => :element,  :via => :delete

  match "/versions/:proj/:grp/:asst/:elclass/:eltype/:elname" => "elements#create_version", :as => :version, :via => :post
  match "/versions/:proj/:grp/:asst/:elclass/:eltype/:elname/:vers" => "elements#destroy_version", :as => :version, :via => :delete

  root :to => 'projects#index'
end
