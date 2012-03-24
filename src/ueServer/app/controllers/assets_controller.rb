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
    @group = Group.get_group(params[:proj], params[:grp])
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
  end

  def destroy
    @asset = Asset.get_asset(params[:proj], params[:grp], params[:asst])

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
