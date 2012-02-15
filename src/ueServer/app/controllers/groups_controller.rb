class GroupsController < ApplicationController
  def index
    @groups = Group.get_groups(params[:project])

    respond_to do |format|
      format.html
      format.json { render :json => @groups }
    end
  end

  def show
    @group = Group.get_group(params[:project], params[:group])

    respond_to do |format|
      format.html
      format.json { render :json => @group }
    end
  end

  def create
    @project = Project.where(:name => params[:project]).first
    @project.groups.create(:name       => params[:name],
                           :path       => params[:path],
                           :created_by => params[:created_by])

    respond_to do |format|
      if @project.save
        format.html
        format.json { render :json => @project,
                      :status => :created }
      else
        format.html
        format.json { render :json => @project.errors,
                      :status => :unprocessable_entity }
      end
    end
  end
end
