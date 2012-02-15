class ElementsController < ApplicationController
  def index
    @elements = Project.where(:name => params[:project]).first.groups.where(
                              :name => params[:group]).first.assets.where(
                              :name => params[:asset]).first.elements

    respond_to do |format|
      format.html
      format.json { render :json => @elements }
    end
  end

  def show
    @element = Project.where(:name => params[:project]).first.groups.where(
                             :name => params[:group]).first.assets.where(
                             :name => params[:asset]).first.elements.where(
                             :elname => params[:elname],
                             :eltype => params[:eltype],
                             :elclass => params[:elclass]).first

    respond_to do |format|
      format.html
      format.json { render :json => @element }
    end
  end

  def create
    @element = Project.where(:name => params[:project]).first.groups.where(
                             :name => params[:group]).first.assets.where(
                             :name => params[:asset]).first.elements.create(
                             :elname => params[:elname],
                             :eltype => params[:eltype],
                             :elclass => params[:elclass],
                             :path => params[:path],
                             :comment => params[:comment],
                             :thumbnail => params[:thumbnail],
                             :created_by => params[:created_by])

    FileUtils.mkdir_p(params[:path])

    respond_to do |format|
      if @element.save
        format.html
        format.json { render :json => @element,
                      :status => :created }
      else
        format.html
        format.json { render :json => @element.errors,
                      :status => :unprocessable_entity }
      end
    end
  end

  def createversion
    @element = Project.where(:name => params[:project]).first.groups.where(
                             :name => params[:group]).first.assets.where(
                             :name => params[:asset]).first.elements.where(
                             :elname => params[:elname],
                             :eltype => params[:eltype],
                             :elclass => params[:elclass]).first

    @element.versions.create(:version => params[:version],
                             :comment => params[:comment],
                             :passes => params[:passes],
                             :thumbnail => params[:thumbnail],
                             :created_by => params[:created_by])

    FileUtils.mkdir_p(params[:path])

    respond_to do |format|
      if @element.save
        format.html
        format.json { render :json => @element,
                      :status => :created }
      else
        format.html
        format.json { render :json => @element.errors,
                      :status => :unprocessable_entity }
      end
    end
  end
end
