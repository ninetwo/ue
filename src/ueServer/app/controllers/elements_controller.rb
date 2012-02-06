class ElementsController < ApplicationController
  def index
    @elements = Element.all(:asset_id => Asset.first(
                            :group_id => Group.first(
                            :name => params[:group],
                            :project_id => Project.first(
                            :name => params[:project])._id)._id)._id)

    respond_to do |format|
      format.html
      format.json { render :json => @elements }
    end
  end

  def show
    @element = Element.first(:elname => params[:elname],
                             :eltype => params[:eltype],
                             :elclass => params[:elclass],
                             :asset_id => Asset.first(
                             :group_id => Group.first(
                             :name => params[:group],
                             :project_id => Project.first(
                             :name => params[:project])._id)._id)._id)

    respond_to do |format|
      format.html
      format.json { render :json => @element }
    end
  end

  def create
    @element = Element.new(:elname => params[:elname],
                           :eltype => params[:eltype],
                           :elclass => params[:elclass],
                           :path => params[:path],
                           :created_by => params[:created_by],
#                           :created_at => params[:created_at],
                           :asset_id => Asset.first(:name => params[:asset],
                                                    :group_id => Group.first(
                                                    :name => params[:group],
                                                    :project_id => Project.first(
                                                    :name => params[:project])._id)._id)._id)

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
    @element = Element.first(:elname => params[:elname],
                             :eltype => params[:eltype],
                             :elclass => params[:elclass],
                             :asset_id => Asset.first(
                             :group_id => Group.first(
                             :name => params[:group],
                             :project_id => Project.first(
                             :name => params[:project])._id)._id)._id)

    @element.versions.build(:version => params[:version],
                            :created_by => params[:created_by],
                            :created_at => params[:created_at])

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
