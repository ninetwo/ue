class GroupsController < ApplicationController
  def index
    @groups = Project.where(:name => params[:project]).first.groups

    respond_to do |format|
      format.html
      format.json { render :json => @groups }
    end
  end

  def show
    @group = Project.where(:name => params[:project]).first.groups.where(:name => params[:group]).first

    respond_to do |format|
      format.html
      format.json { render :json => @group }
    end
  end

  def create
    @group = Project.where(:name => params[:project]).first.groups.create(
                           :name       => params[:name],
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
