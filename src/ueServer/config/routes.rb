UeServer::Application.routes.draw do
  match "/projects"                      => "projects#index",   :as => :projects, :via => :get
  match "/projects"                      => "projects#create",  :as => :projects, :via => :post
  match "/projects"                      => "projects#update",  :as => :projects, :via => :put
  match "/projects"                      => "projects#destroy", :as => :projects, :via => :destroy
  match "/projects/:project"             => "projects#show",    :as => :projects

  match "/groups/:project"               => "groups#index",   :as => :groups, :via => :get
  match "/groups/:project"               => "groups#create",  :as => :groups, :via => :post
  match "/groups/:project"               => "groups#update",  :as => :groups, :via => :put
  match "/groups/:project"               => "groups#destroy", :as => :groups, :via => :destroy
  match "/groups/:project/:group"        => "groups#show",    :as => :groups

  match "/assets/:project/:group"        => "assets#index",   :as => :assets, :via => :get
  match "/assets/:project/:group"        => "assets#create",  :as => :assets, :via => :post
  match "/assets/:project/:group"        => "assets#update",  :as => :assets, :via => :put
  match "/assets/:project/:group"        => "assets#destroy", :as => :assets, :via => :destroy
  match "/assets/:project/:group/:asset" => "assets#show",    :as => :assets

  match "/elements/:project/:group/:asset"                          => "elements#index"
  match "/elements/:project/:group/:asset/:elclass/:eltype/:elname" => "elements#show",    :via => :get
  match "/elements/:project/:group/:asset/:elclass/:eltype/:elname" => "elements#create",  :via => :post
  match "/elements/:project/:group/:asset/:elclass/:eltype/:elname" => "elements#update",  :via => :put
  match "/elements/:project/:group/:asset/:elclass/:eltype/:elname" => "elements#destroy", :via => :destroy

  match "/versions/:project/:group/:asset/:elclass/:eltype/:elname" => "elements#createversion",  :via => :post

  match "/config/:project(/:group(/:asset(/:elclass(/:eltype(/:elname)))))" => "configs#show", :as => :config, :via => :get
  match "/config/:project(/:group(/:asset(/:elclass(/:eltype(/:elname)))))" => "configs#create", :as => :config, :via => :post
  match "/config/:project(/:group(/:asset(/:elclass(/:eltype(/:elname)))))" => "configs#update", :as => :config, :via => :put
  match "/config/:project(/:group(/:asset(/:elclass(/:eltype(/:elname)))))" => "configs#destroy", :as => :config, :via => :destroy

  root :to => 'projects#index'
end
