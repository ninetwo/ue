class ElementsController < ApplicationController
  def index
    @elements = Element.get_elements(params[:project], params[:group], params[:asset])

    respond_to do |format|
      format.html
      format.json { render :json => @elements }
    end
  end

  def show
    @element = Element.get_element(params[:project], params[:group], params[:asset],
                                   params[:elname], params[:eltype], params[:elclass])

    respond_to do |format|
      format.html
      format.json { render :json => @element }
    end
  end

  def create
    @asset = Asset.get_asset(params[:project], params[:group], params[:asset])
    @asset.elements.new(:elname     => params[:elname],
                        :eltype     => params[:eltype],
                        :elclass    => params[:elclass],
                        :path       => params[:path],
                        :comment    => params[:comment],
                        :thumbnail  => params[:thumbnail],
                        :created_by => params[:created_by])

    FileUtils.mkdir_p(params[:path])

    respond_to do |format|
      if @asset.save
        format.html
        format.json { render :json => @asset,
                      :status => :created }
      else
        format.html
        format.json { render :json => @asset.errors,
                      :status => :unprocessable_entity }
      end
    end
  end

  def create_version
    @element = Element.get_element(params[:project], params[:group], params[:asset],
                                   params[:elname], params[:eltype], params[:elclass])
    @element.versions.new(:version    => params[:version],
                          :comment    => params[:comment],
                          :passes     => params[:passes],
                          :thumbnail  => params[:thumbnail],
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
