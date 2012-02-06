class ProjectsController < ApplicationController
  def index
    @projects = Project.all

    respond_to do |format|
      format.html
      format.json { render :json => @projects }
    end
  end

  def show
    @project = Project.first(:name => params[:project])

    respond_to do |format|
      format.html
      format.json { render :json => @project }
    end
  end

  def create
    @project = Project.new(:name       => params[:name],
                           :path       => params[:path],
                           :created_by => params[:created_by],
                           :created_at => params[:created_at])

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
