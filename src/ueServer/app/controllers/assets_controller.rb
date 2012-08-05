class AssetsController < ApplicationController
  def index
    @assets = Asset.get_assets(params[:proj], params[:grp])

    respond_to do |format|
      format.html
      format.json { render :json => @assets }
    end
  end

  def show
    @asset = Asset.get_asset(params[:proj], params[:grp], params[:asst])

    respond_to do |format|
      format.html
      format.json { render :json => @asset }
    end
  end

  def create
    @group = Project.where(:name => params[:proj]).first.groups.where(
                           :name => params[:grp]).first
    @asset = @group.assets.new(params[:asset])

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

  def update
    @asset = Project.where(:name => params[:proj]).first.groups.where(
                           :name => params[:grp]).first.assets.where(
                           :name =>  params[:asst]).first
    @asset.update_attributes(params[:asset])

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

  def destroy
    @asset = Project.where(:name => params[:proj]).first.groups.where(
                           :name => params[:grp]).first.assets.where(
                           :name =>  params[:asst]).first

    respond_to do |format|
      if @asset.destroy
        format.html
        format.json { render :json => @asset,
                      :status => :ok }
      else
        format.html
        format.json { render :json => @asset.errors,
                      :status => :unprocessable_entity }
      end
    end
  end
end
