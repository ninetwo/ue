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
    @project = Project.where(:name => params[:proj]).first
    @group = @project.groups.new(:name       => params[:name],
                                 :group_type => params[:group_type],
                                 :created_by => params[:created_by],
                                 :path       => params[:path])

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
  end
end
