class AssetsController < ApplicationController
  def index
    @assets = Asset.get_assets(params[:project], params[:group])

    respond_to do |format|
      format.html
      format.json { render :json => @assets }
    end
  end

  def show
    @asset = Asset.get_asset(params[:project], params[:group], params[:asset])

    respond_to do |format|
      format.html
      format.json { render :json => @asset }
    end
  end

  def create
    @group = Group.get_group(params[:project], params[:group])
    @group.assets.new(:name       => params[:name],
                      :path       => params[:path],
                      :created_by => params[:created_by])

    respond_to do |format|
      if @group.save
        format.html
        format.json { render :json => @group,
                      :status => :created }
      else
        format.html
        format.json { render :json => @group.errors,
                      :status => :unprocessable_entity }
      end
    end
  end
end
