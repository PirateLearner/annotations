$(document).ready(function(){
		
	var fixtures = {};
	
	fixtures = [
		             	{
							content_type: "9",
							object_id: "1",
							paragraph: "1",
							body: "Lorem Ipsum",
							privacy: "3",
							privacy_override:"0",
							author : {
								id: "1",
								username: "John Doe",
								gravatar: "images/male.png",
								url: "#",
									},
							shared_with: ["1"],
		             	},
						{	
		             		content_type: "9",
							object_id: "1",
							paragraph: "1",
							body: "Your documentation source should be written as regular Markdown files, and placed in a directory somewhere in your project."+ 
	                                         "Normally this directory will be named docs and will exist at the top level of your project,alongside the mkdocs.yml configuration file.",
 							privacy: "3",
							privacy_override:"0",
							author : {
								id: "2",
								username: "Someone Else",
								gravatar: "images/female.png",
								url: "#",
									},
						},
						{	
							content_type: "9",
							object_id: "1",
							paragraph: "6",
							body: "But we have to make tradeoffs to make something work",
							privacy: "3",
							privacy_override:"0",
							author : {
								id: "1",
								username: "John Doe",
								gravatar: "images/male.png",
								url: "#",
									},
						},
						{	
							content_type: "9",
							object_id: "1",
							paragraph: "5",
							body: "Lorem Ipsum",
							privacy: "3",
							privacy_override:"0",
							author : {
								id: "1",
								username: "John Doe",
								gravatar: "images/male.png",
								url: "#",
									},
						},
						{	
							content_type: "9",
							object_id: "1",
							paragraph: "5",
							body: "But we have to make tradeoffs to make something work",
							privacy: "3",
							privacy_override:"0",
							author : {
								id: "2",
								username: "Someone Else",
								gravatar: "images/female.png",
								url: "#",
									},
						},
						{	
							content_type: "9",
							object_id: "1",
							paragraph: "3",
							body: "Lorem Ipsum",
							privacy: "3",
							privacy_override:"0",
							author : {
								id: "1",
								username: "John Doe",
								gravatar: "images/male.png",
								url: "#",
									},
						}
					];
	
	
	var getCookie = function(name){
	    var cookieValue = null;
	    if (document.cookie && document.cookie != '') {
	        var cookies = document.cookie.split(';');
	        for (var i = 0; i < cookies.length; i++) {
	            var cookie = jQuery.trim(cookies[i]);
	            // Does this cookie string begin with the name we want?
	            if (cookie.substring(0, name.length + 1) == (name + '=')) {
	                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
	                break;
	            }
	        }
	    }
	    return cookieValue;
	};
	
	var csrfSafeMethod = function(method) {
	    // these HTTP methods do not require CSRF protection
	    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	};
	
	var annotations = {};
	annotations.csrftoken = getCookie('csrftoken');
	annotations.currentAnnotation = 0;
		
	annotations.currentUser = {
								id: "0",
								username: "John Doe",
								gravatar: "images/male.png",
								url: "#",
							};
	
	var getCurrentUser = function(){
		
	    $.ajaxSetup({
	        beforeSend: function(xhr, settings) {
	            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
	                xhr.setRequestHeader("X-CSRFToken", annotations.csrftoken);
	            }
	        }
	    });
	    //Save Form Data........
	    $.ajax({
	        cache: false,
	        url : "/annotations/users/current/",
	        type: "GET",
	        dataType : "json",
	        
	        success : function(data){
	        	if(!('id' in data)){
	        		annotations.currentUser = {
							id: "0",
							username: "Guest",
							gravatar: "images/male.png",
							url: "#",
						};
	        	}
	        	else{
	        	annotations.currentUser = {
						id: data['id'],
						username: data['username'],
						gravatar: data['gravatar'],
						url: "#",
					};
	        	}
	        	
	        	//console.log(annotations.currentUser);
	        },
	        error : function (xhRequest, ErrorText, thrownError) {
	            //alert("Failed to process annotation correctly, please try again");
	            console.log('xhRequest: ' + xhRequest + "\n");
	            console.log('ErrorText: ' + ErrorText + "\n");
	            console.log('thrownError: ' + thrownError + "\n");
	        }
	    });	
	};
	
	annotations.formElement = $('<div class="comments-form-block">'+
                        '<form class="comments-form" id="annotation_form">'+
                            '<textarea id="comments-form-text" class="comments-form--user-input"'+ 
                                    'placeholder="Make a note" form="annotation_form" cols="40" rows="3" maxlength="500"'+
                                    'required="True"></textarea>'+
                            '<button id="comments-form-submit" class="comments-submit" type="button">Submit</button>'+
                        '</form>'+
                    '</div>');
	
	
	/**
	 * showForm
	 * 
	 * @brief Attaches the form to the current content block
	 */
	var showForm = function(id){
		//console.log('Show form in '+id);
		
		//console.log($('.comments-form-block'));
		if($('.comments-form-block').length != 0){
			/* The form has been attached somewhere. */
			/* Clear out form contents, if any. */
			
			//console.log('Attached elsewhere');
			annotations.formElement.find($('#comments-form-text')).val('');
			
			if(parseInt($('.comments-form-block').parent('.annotation--container').attr('data-section-id'))!=id){
				hideForm();
			}
		}
		/* Else it is pointing to the object not yet appended */
		$('*[data-section-id="'+id+'"]').find('.comments-container').prepend(annotations.formElement);	
		/*
		 * bind the postAnnotation to the form button.
		 */
		annotations.formElement.find("#comments-form-submit").on('click', postAnnotation);
//		console.log('Printing');
//		console.log($('.comments-form-block'));
	};
	
	var hideForm = function(){
		//console.log('Hide Form');
		if($('.comments-form-block').length >0){
			annotations.formElement = $('.comments-form-block');
			/*
			 * unbind event
			 */
			annotations.formElement.find("#comments-form-submit").unbind('click', postAnnotation);
			annotations.formElement.detach();			
		}
	};
	
	/**
	 * postAnnotation
	 * @brief : Posts an annotation.
	 * 
	 * This is a fixture right now, all it does is receive and check sanity of annotation and call the
	 * renderAnnotation method as if the server responded with a valid response.
	 */
	var postAnnotation = function(e){
		//console.log('postAnnotation');
		/* Construct a JSON string of the data in annotation. */
		//console.log(this);
		
		/* First find the parent's para-id */
		id = parseInt($(this).parents(".annotation--container").attr("data-section-id"));
		//console.log("Para ID: "+ id);
		
		/* Current text must not be empty. Though this must be taken care of in HTML5 required flag*/
		body = $("#comments-form-text").val();
		//console.log(body);
		if(body === ''){
			console.log('Error. Body has no content.')
			return;
		}
		
		data = {
				body: body,
				paragraph: id,
				content_type: "9",
				object_id: "1",
				privacy: "3",
				privacy_override:"0",
				shared_with: [],
			};
		
		/* POST it now! */
		//Form Validation goes here....

	    $.ajaxSetup({
	        beforeSend: function(xhr, settings) {
	            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
	                xhr.setRequestHeader("X-CSRFToken", annotations.csrftoken);
	            }
	        }
	    });
	    //Save Form Data........
	    $.ajax({
	        cache: false,
	        url : "http://127.0.0.1:8000/annotations/annotations/",
	        type: "POST",
	        dataType : "json",
	        contentType: "application/json;",
	        data : JSON.stringify(data),
	        context : this,
	        success : renderSingleAnnotation,
	        error : function (xhRequest, ErrorText, thrownError) {
	            //alert("Failed to process annotation correctly, please try again");
	            console.log('xhRequest: ' + xhRequest + "\n");
	            console.log('ErrorText: ' + ErrorText + "\n");
	            console.log('thrownError: ' + thrownError + "\n");
	        }
	    });	
		
		/* create a fixture */
		/*
		content = [
					{
						content_type: "9",
						object_id: "1",
						paragraph: id,
						body: body,
						privacy: "3",
						privacy_override:"0",
						user : {
							id: "1",
							username: "John Doe",
							gravatar: "images/male.png",
							url: "#",
								},
		         	}
				];
		*/
		/* Return object */
		//renderAnnotations(content);
		/* Clear out form contents, if any. */
		annotations.formElement.find($('#comments-form-text')).val('');
	}
	
	var toggleOtherAnnotations = function(e){
		if($(this).hasClass('folded')){
			/* Unfold the annotations */
			$(this).removeClass('folded').addClass('unfolded')
			$(this).next().removeClass('hidden');
		}
		else{
			/* Fold the annotations */
			$(this).removeClass('unfolded').addClass('folded')
			$(this).next().addClass('hidden');			
		}
		
	}
	
	/**
	 * removeAnnotation
	 * @param data
	 */
	var removeAnnotation = function(data){
		//console.log('Remove Annotation response');
		//console.log(data);
	};
	
	/**
	 * deleteAnnotation
	 * @param id: ID of paragraph to remove
	 */
	var deleteAnnotation = function(id){
		id= parseInt($(this).attr('data-comment-id'));
		//console.log('Deleting annotation' + id);
		
		$.ajaxSetup({
	        beforeSend: function(xhr, settings) {
	            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
	                xhr.setRequestHeader("X-CSRFToken", annotations.csrftoken);
	            }
	        }
	    });
	    //Save Form Data........
	    $.ajax({
	        cache: false,
	        url : "http://127.0.0.1:8000/annotations/annotations/"+id+"/",
	        type: "DELETE",
	        dataType : "json",
	        contentType: "application/json;",
	        //data : JSON.stringify(data),
	        context : this,
	        success : removeAnnotation,
	        error : function (xhRequest, ErrorText, thrownError) {
	            //alert("Failed to process annotation correctly, please try again");
	            console.log('xhRequest: ' + xhRequest + "\n");
	            console.log('ErrorText: ' + ErrorText + "\n");
	            console.log('thrownError: ' + thrownError + "\n");
	        }
	    });	
	    
	    /* Update annotation count on adjoining container */
	    //console.log($(this).closest('.comments').find('.comments--toggle p'));
	    commentCount = parseInt($(this).closest('.comments').find('.comments--toggle p').text());
	    //console.log('Comment Count now is '+ commentCount);
	    if((commentCount -1)==0){
	    	$(this).closest('.comments').find('.comments--toggle p').text('+');
	    }
	    else{
	    	$(this).closest('.comments').find('.comments--toggle p').text(commentCount -1);
	    }
	    
	    /* Remove the annotation from flow */
	    $(this).closest('.comments-container-item').remove();

	};
	/**
	 * renderSingleAnnotation
	 * @param data : Payload received from the server
	 * @brief Loads annotations in their respective containers.
	 * 
	 */
	var renderSingleAnnotation = function(data){
		data_list = [data];
		renderAnnotations(data_list);
	}
	/**
	 * renderAnnotations
	 * @param data : Payload received from the server
	 * @brief Loads annotations in their respective containers.
	 * 
	 */
	var renderAnnotations = function(data){
		//console.log('renderAnnotations');
		//console.log('Data received: ');
		//console.log(data);
		//console.log('Length: '+ data.length);
		if (annotationCopy == null){
			/* Create a fresh copy of the variable*/
			//console.log('It is null. Make a new one');
			annotationCopy = $('#commentable-container');
			//console.log(annotationCopy);
		}
		for(i=0; i< data.length;i++){
//			console.log(annotationCopy.children('[data-section-id="'+data[i]['paragraph_id']+'"]'));
			/* Find the parent container */

			currentObject = annotationCopy.children('[data-section-id="'+data[i]['paragraph']+'"]');
			/* Find the annotations container inside that and append the comment */
			currentComment = $('<div class="comments-container-item">'+
                    			'<div class="comments-container--media">'+
                    				'<img class="comments-author-image" src=""/>'+
            					'</div>'+
            					'<div class="comments-container--block">'+
            					'<a class="comments-author-link" href="#"><span class="comments-author-name"></span></a>'+
            					'<span class="comments-container--text"></span>'+
            					'<div class="comments-control-box">'+
            					'<span class="comments-control comments-delete">Delete</span>'+
            					'<span class="comments-control">Shared with</span>'+
            					'</div>'+
            					'<span class="comments-delete glyphicon glyphicon-remove"></span>'+
            					'</div>'+
            					'</div>');
			
			/* Create the annotation */
			currentComment.find('.comments-author-image').attr('src', data[i]['author']['gravatar']);
			currentComment.find('.comments-author-name').text(data[i]['author']['username']);
			currentComment.find('.comments-author-link').attr('href',data[i]['author']['url']);
			currentComment.find('.comments-container--text').text(data[i]['body']);
			currentComment.find('.comments-delete').attr('data-comment-id', data[i]['id']);
			
			currentComment.find('.comments-delete').on('click', deleteAnnotation);
			/* Also add to main container if the user is a guest. */
			if((parseInt(data[i]['author']['id']) === parseInt(annotations.currentUser['id']))||
					(parseInt(annotations.currentUser['id'])===0)){
				/* Append to main visible list*/
				currentObject.find('[id *="user_annotations_"]').append(currentComment);
			}
			else{
				/* Append to the folded list */
				currentObject.find('[id *="other_annotations_"]').append(currentComment);
				/* Now that we have other annotations, unhide the show button too */
				console.log('Unhide the button');
				
				if(currentObject.find('.comments-bucket-toggle').hasClass('hidden')){
					currentObject.find('.comments-bucket-toggle').removeClass('hidden');
					/* Bind event to show fold or unfold other annotations*/
					currentObject.find('.comments-bucket-toggle').on('click', toggleOtherAnnotations);
				}				
				
				if(!currentObject.find('.comments-bucket-toggle').hasClass('unfolded')){
					currentObject.find('.comments-bucket-toggle').removeClass('unfolded');
					currentObject.find('.comments-bucket-toggle').addClass('folded');
				}
			}
			/* Also append it to the bucket list.*/
			$('#article-adjunct-tab-notes').append(currentComment.clone());
			
			/* Update the annotation count on the button */
			temp = currentObject.find('.comments--toggle p').text();
			//console.log('Comment Count is ' +temp);
			commentCount = ((temp = currentObject.find('.comments--toggle p').text()) ==='+') ? 1 : (parseInt(temp)+1);
			//console.log(currentObject.find('.comments-container'));
			currentObject.find('.comments--toggle p').text(commentCount);
			if(!currentObject.find('.comments--toggle').hasClass('has-annotations') && commentCount > 0)
			{
				currentObject.find('.comments--toggle').addClass('has-annotations');
			}
			//console.log('Updated comment count to '+ commentCount);
		}
		/* Put the variable back to sleep now */
		annotationCopy = null;
	};
	
	
	/*
	 * Load Annotations
	 */
	var loadAnnotations = function(){
		/*
		 * At some point of time, this method will be making Ajax queries. For now, it is just calls renderAnnotations directly by passing fixtures.
		 */
		//renderAnnotations(fixtures);
		$.ajax({
		    // the URL for the request
		    url: 'http://127.0.0.1:8000/annotations/blogcontent/1/comments/',
		 
		    // the data to send (will be converted to a query string)
		    data: {
		        format:'json'
		    },
		 
		    // whether this is a POST or GET request
		    type: "GET",
		 
		    // the type of data we expect back
		    dataType : "json",
		 
		    // code to run if the request succeeds;
		    // the response is passed to the function
		    success: renderAnnotations,
		 
		    // code to run if the request fails; the raw request and
		    // status codes are passed to the function
		    error: function( xhr, status, errorThrown ) {
		        //alert( "Sorry, there was a problem!" );
		        console.log( "Error: " + errorThrown );
		        console.log( "Status: " + status );
		        console.dir( xhr );
		    },
		 
		    // code to run regardless of success or failure
		    complete: function( xhr, status ) {
		        //alert( "The request is complete!" );
		    }
		});
	};
	
	
	/**
	 * toggleAnnotations
	 * @param event 
	 * @brief Hides or unhides the annotations depending on their current state.
	 * @detail TODO
	 */
	annotations.toggleAnnotations = function(e){
		/* 
		 * If the clicked annotation is the same is the one that was active, we need to close its annotations only,
		 * otherwise we must close it and open the currently active's annotations.
		 */
		activeID = parseInt($(this).parents('.annotation--container').attr('data-section-id'));
		
		/* Hide all other annotations first */
		$('.comments').children('.comments-container').addClass('hidden');
		/* If we clicked on the same bubble, it must collapse, and we return to initial state */
		if(annotations.currentAnnotation === activeID ){
			/* Remove the higlight class from the bubble: .annotation-highlight */
			$(this).removeClass('annotation-highlight');
			$(this).parents("#commentable-container").removeClass('annotations-active');
			annotations.currentAnnotation = 0;
			/*
			 * Unbind 'click anywhere' also from the entire document
			 */
			$(document).unbind('click');
			
			/* hide the form too */
			hideForm();
			return;
		}
		
		/* Else, we've selected a new bubble (and have already hidden everything.)*/
		/* 
		 * We could first find the previous object to remove the annotation-highlight class from it
		 * or we could directly ask jquery to remove that class from all.
		 * That is one reason why Jquery makes things seem very simple, though it might be a preformance hit
		 * internally. 
		 */
		//$('.comments--toggle').removeClass('annotation-highlight');
		/*
		 * If there is no previous annotation selected, then we must bind a 'click anywhere to close' 
		 * event to document.
		 */
		if(annotations.currentAnnotation === 0){
			$(document).on('click', function(e) {
				//console.log($(event.target));
				//console.log($(event.target).closest('.side-comment').length);

				/*
				 * If the element we clicked on is not close to the comments,
				 * close the annotations then.
				 */
				if (!($(e.target).closest('.comments').length)){
					/* Hide all other annotations */
					$('.comments').children('.comments-container').addClass('hidden');
					$('*[data-section-id="'+annotations.currentAnnotation+'"]').find('.comments--toggle').removeClass('annotation-highlight');
					$('#commentable-container').removeClass('annotations-active');
					/* Reset the currently selected Annotation state */
					annotations.currentAnnotation = 0;
					/* Also hide the form */
					hideForm();
					/* unbind this listener too*/
					$(document).unbind('click');
				}
			});
		}
		
		/* OR the other method */
		$('*[data-section-id="'+annotations.currentAnnotation+'"]').find('.comments--toggle').removeClass('annotation-highlight');
		/* Update state variable */
		annotations.currentAnnotation = parseInt($(this).parents('.annotation--container').attr('data-section-id'));
//		console.log('Current Annotation is: ' + annotations.currentAnnotation);
		/* find the parent with classname 'comments' */
		$(this).addClass('annotation-highlight');
		$(this).parent('.comments').children('.comments-container').removeClass('hidden');
		
		/* Add class annotations-active to the parent with ID commentable-container */
		if(!$(this).parents("#commentable-container").hasClass('annotations-active')){
			$(this).parents("#commentable-container").addClass('annotations-active');
		}
		
		/* show the form too */
		showForm(activeID);
	};
	
	var bindAnnotations = function(){
		/* Find all annotation toggle buttons and bind the click event to them. */
		$('.comments--toggle').on('click', annotations.toggleAnnotations );
//		console.log('Binding complete');
	};
	
	var wrapContent = function(){
		index = parseInt($(this).attr('id'));
		
//		console.log('Paragraph ID: '+index);
		$(this).wrap('<div data-section-id="'+index+'" class="annotation--container clearfix"></div>');
		$('<div class="comments clearfix">'+
                '<h3 class="comments--toggle rectangular-speech"><p>+</p></h3>'+
                '<div class="comments-container hidden">'+
                '<div class="comments-container-bucket" id="user_annotations_'+index+'"></div>'+
                '<button class="comments-bucket-toggle folded hidden" type="button"> other annotations</button>'+
                '<div class="comments-container-bucket hidden" id="other_annotations_'+index+'"></div>'+
                '</div>'+
                '</div>').insertAfter($(this));
	};
	/*
	 * Find the master container, and remove its children from flow.
	 * Do not remove the container from the flow, for we don't want to keep track of its parent for re-insert.
	 * 
	 * On second thoughts, it would be a painful thing to do in Jquery. What we want is that the reflow of DOM must take 
	 * place the least number of times it is possible. The wrap function for each element would cause reflow, which isn't good.
	 * 
	 * So, we'll clone the overall container in Jquery, work on this clone, and when everything is done, we'll replace the 
	 * original one with its upgraded clone.
	 */
	
	/* 
	 * using true,true for clone because we are not assuming that the previous content will be purely html with no event handlers. 
	 */
	var annotationCopy = $('#commentable-container').clone(true,true);
	
	/*
	 * Here, we're assuming that only immediate level content blocks have IDs and need annotations.
	 * Loop through the children, wrapping them in a div first, and append annotations container after them inside the wrapping. 
	 */
	annotationCopy.children().each(wrapContent);
	
	/*
	 * Load annotations
	 */
	loadAnnotations();
	
	$('#commentable-container').replaceWith(annotationCopy);
	
	annotationCopy = null;
	/*
	 * Now bind to annotation buttons for clicks
	 */
	bindAnnotations();	
	
	/*
	 * Handle tabs
	 */
	$('.article-adjunct-nav--item a').on('click', function(e)  {
        var currentAttrValue = $(this).attr('href');
 
        // Show/Hide Tabs
        $(currentAttrValue).show().siblings().hide();
 
        // Change/remove current tab to active
        $(this).parent('li').addClass('active').siblings().removeClass('active');
 
        e.preventDefault();
    });
	
	/* Get the current user */
	getCurrentUser();
});