class GroupsController < ApplicationController
  def index
    @groups = Group.all(:project_id => Project.first(
                        :name => params[:project])._id)

    respond_to do |format|
      format.html
      format.json { render :json => @groups }
    end
  end

  def show
    @group = Group.first(:name => params[:group],
                         :project_id => Project.first(
                         :name => params[:project])._id)

    respond_to do |format|
      format.html
      format.json { render :json => @group }
    end
  end

  def create
    @group = Group.new(:name       => params[:name],
                       :path       => params[:path],
                       :created_by => params[:created_by],
                       :project_id => Project.first(:name => params[:project])._id)

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
