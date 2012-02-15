class AssetsController < ApplicationController
  def index
    @assets = Project.where(:name => params[:project]).first.groups.where(:name => params[:group]).first.assets

    respond_to do |format|
      format.html
      format.json { render :json => @assets }
    end
  end

  def show
    @asset = Project.where(:name => params[:project]).first.groups.where(:name => params[:group]).first.assets.where(:name => params[:asset]).first

    respond_to do |format|
      format.html
      format.json { render :json => @asset }
    end
  end

  def create
    @asset = Project.where(:name => params[:project]).first.groups.where(:name => params[:group]).first.assets.create(
                          :name       => params[:name],
                          :path       => params[:path],
                          :created_by => params[:created_by])

    respond_to do |format|
      if @asset.save
        format.html
        format.json { render :json => @asset,
                      :status => :created }
      else
        format.html
        format.json { render :json => @asset.errors,
                      :status => :unprocessable_entity }
      end
    end
  end
end
