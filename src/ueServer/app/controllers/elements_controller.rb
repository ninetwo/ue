class ElementsController < ApplicationController
  def index
    @elements = Element.get_elements(params[:proj], params[:grp], params[:asst])

    respond_to do |format|
      format.html
      format.json { render :json => @elements }
    end
  end

  def show
    @element = Element.get_element(params[:proj], params[:grp], params[:asst],
                                   params[:elclass], params[:eltype], params[:elname])

    respond_to do |format|
      format.html
      format.json { render :json => @element }
    end
  end

  def create
    @asset = Project.where(:name => params[:proj]).first.groups.where( 
                           :name => params[:grp]).first.assets.where( 
                           :name =>  params[:asst]).first
    @element = @asset.elements.new(:elname     => params[:elname],
                                   :eltype     => params[:eltype],
                                   :elclass    => params[:elclass],
                                   :comment    => params[:comment],
                                   :thumbnail  => params[:thumbnail],
                                   :created_by => params[:created_by])

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

  def create_version
    @element = Project.where(:name => params[:proj]).first.groups.where(
                             :name => params[:grp]).first.assets.where(
                             :name =>  params[:asst]).first.elements.where(
                             :elclass => params[:elclass],
                             :eltype => params[:eltype],
                             :elname => params[:elname]).first
    @version = @element.versions.new(:version    => params[:version],
                                     :comment    => params[:comment],
                                     :passes     => params[:passes],
                                     :thumbnail  => params[:thumbnail],
                                     :created_by => params[:created_by])

    respond_to do |format|
      if @version.save
        format.html
        format.json { render :json => @version,
                      :status => :created }
      else
        format.html
        format.json { render :json => @version.errors,
                      :status => :unprocessable_entity }
      end
    end
  end

  def update
  end

  def destroy
  end
end
