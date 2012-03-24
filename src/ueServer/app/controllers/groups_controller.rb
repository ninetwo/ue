class GroupsController < ApplicationController
  def index
    @groups = Group.get_groups(params[:proj])

    respond_to do |format|
      format.html
      format.json { render :json => @groups }
    end
  end

  def show
    @group = Group.get_group(params[:proj], params[:grp])

    respond_to do |format|
      format.html
      format.json { render :json => @group }
    end
  end

  def create
    @project = Project.get_project(params[:proj])
    @group = @project.groups.new(params[:group])

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

  def update
  end

  def destroy
    @group = Group.get_group(params[:proj], params[:grp])

    respond_to do |format|
      if @group.destroy
        format.html
        format.json { render :json => @group,
                      :status => :ok }
      else
        format.html
        format.json { render :json => @group.errors,
                      :status => :unprocessable_entity }
      end
    end
  end
end
