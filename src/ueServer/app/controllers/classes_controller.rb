class ClassesController < ApplicationController
  def index
    @classes = Class.all(:asset_id => Asset.first(:group_id => Group.first(:name => params[:group], :project_id => Project.first(:name => params[:project])._id)._id)._id)

    respond_to do |format|
      format.html
      format.json { render :json => @classes }
    end
  end

  def create
    @asset = Asset.new(:name       => params[:name],
                       :path       => params[:path],
                       :created_by => params[:created_by],
                       :created_at => params[:created_at],
                       :group_id   => Group.first(:name => params[:group], :project_id => Project.first(:name => params[:project])._id)._id)

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
