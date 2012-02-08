UeServer::Application.routes.draw do
  match "/config/:project(/:group(/:asset(/:elclass(/:eltype(/:elname)))))" => "configs#show", :as => :config, :via => :get
  match "/config/:project(/:group(/:asset(/:elclass(/:eltype(/:elname)))))" => "configs#create", :as => :config, :via => :post
  match "/config/:project(/:group(/:asset(/:elclass(/:eltype(/:elname)))))" => "configs#update", :as => :config, :via => :put
  match "/config/:project(/:group(/:asset(/:elclass(/:eltype(/:elname)))))" => "configs#destroy", :as => :config, :via => :destroy

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

  root :to => "projects#index"

  # The priority is based upon order of creation:
  # first created -> highest priority.

  # Sample of regular route:
  #   match 'products/:id' => 'catalog#view'
  # Keep in mind you can assign values other than :controller and :action

  # Sample of named route:
  #   match 'products/:id/purchase' => 'catalog#purchase', :as => :purchase
  # This route can be invoked with purchase_url(:id => product.id)

  # Sample resource route (maps HTTP verbs to controller actions automatically):
  #   resources :products

  # Sample resource route with options:
  #   resources :products do
  #     member do
  #       get 'short'
  #       post 'toggle'
  #     end
  #
  #     collection do
  #       get 'sold'
  #     end
  #   end

  # Sample resource route with sub-resources:
  #   resources :products do
  #     resources :comments, :sales
  #     resource :seller
  #   end

  # Sample resource route with more complex sub-resources
  #   resources :products do
  #     resources :comments
  #     resources :sales do
  #       get 'recent', :on => :collection
  #     end
  #   end

  # Sample resource route within a namespace:
  #   namespace :admin do
  #     # Directs /admin/products/* to Admin::ProductsController
  #     # (app/controllers/admin/products_controller.rb)
  #     resources :products
  #   end

  # You can have the root of your site routed with "root"
  # just remember to delete public/index.html.
  # root :to => 'welcome#index'

  # See how all your routes lay out with "rake routes"

  # This is a legacy wild controller route that's not recommended for RESTful applications.
  # Note: This route will make all actions in every controller accessible via GET requests.
  # match ':controller(/:action(/:id))(.:format)'
end
