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
#    @project = Project.new(:name       => params[:name],
#                           :created_by => params[:created_by],
#                           :path       => params[:path])
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

    if params[:name] != nil
      @project.name = params[:name]
    end
    if params[:path] != nil
      @project.path = params[:path]
    end
    if params[:created_by] != nil
      @project.created_by = params[:created_by]
    end

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
  end
end
