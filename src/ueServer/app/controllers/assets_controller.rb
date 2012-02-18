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
#    @asset = @group.assets.new(:name       => params[:name],
#                               :asset_type => params[:asset_type],
#                               :created_by => params[:created_by],
#                               :path       => params[:path],
#                               :startFrame => params[:startFrame],
#                               :endFrame   => params[:endFrame])
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
  end
end
