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
#    @asset = Project.where(:name => params[:proj]).first.groups.where( 
#                           :name => params[:grp]).first.assets.where( 
#                           :name =>  params[:asst]).first
    @asset = Asset.get_asset(params[:proj], params[:grp], params[:asst])
    @element = @asset.elements.new(params[:element])
    @element.elclass = params[:elclass]
    @element.eltype = params[:eltype]
    @element.elname = params[:elname]

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
    @version = @element.versions.new(params[:version])

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
    @element = Project.where(:name => params[:proj]).first.groups.where(
                             :name => params[:grp]).first.assets.where(
                             :name =>  params[:asst]).first.elements.where(
                             :elclass => params[:elclass],
                             :eltype => params[:eltype],
                             :elname => params[:elname]).first

    respond_to do |format|
      if @element.destroy
        format.html
        format.json { render :json => @element,
                      :status => :ok }
      else
        format.html
        format.json { render :json => @element.errors,
                      :status => :unprocessable_entity }
      end
    end
  end

  def destroy_version
    @version = Project.where(:name => params[:proj]).first.groups.where(
                             :name => params[:grp]).first.assets.where(
                             :name =>  params[:asst]).first.elements.where(
                             :elclass => params[:elclass],
                             :eltype => params[:eltype],
                             :elname => params[:elname]).first.versions.where(
                             :version => params[:vers]).first

    respond_to do |format|
      if @version.destroy
        format.html
        format.json { render :json => @version,
                      :status => :ok }
      else
        format.html
        format.json { render :json => @version.errors,
                      :status => :unprocessable_entity }
      end
    end
  end
end
