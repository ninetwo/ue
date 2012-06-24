class ProjectsController < ApplicationController
  def index
    @projects = Project.all

    respond_to do |format|
      format.html
      format.json { render :json => @projects }
    end
  end

  def show
    @project = Project.get_project(params[:proj])

    respond_to do |format|
      format.html
      format.json { render :json => @project }
    end
  end

  def create
    @project = Project.new(params[:project])

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

  def update
    @project = Project.get_project(params[:proj])

    respond_to do |format|
      if @project.update_attributes
        format.html
        format.json { head :no_content }
      else
        format.html
        format.json { render :json => @project.errors,
                      :status => :unprocessable_entity }
      end
    end
  end

  def destroy
    @project = Project.get_project(params[:proj])

    respond_to do |format|
      if @project.destroy
        format.html
        format.json { render :json => @project,
                      :status => :ok }
      else
        format.html
        format.json { render :json => @project.errors,
                      :status => :unprocessable_entity }
      end
    end
  end
end
