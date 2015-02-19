$(document).ready(function(){
	
	var annotations = {};
	annotations.currentAnnotation = 0;
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
		
		/* OR the other method */
		$('*[data-section-id="'+annotations.currentAnnotation+'"]').find('.comments--toggle').removeClass('annotation-highlight');
		/* Update state variable */
		annotations.currentAnnotation = parseInt($(this).parents('.annotation--container').attr('data-section-id'));
		console.log('Current Annotation is: ' + annotations.currentAnnotation);
		/* find the parent with classname 'comments' */
		$(this).addClass('annotation-highlight');
		$(this).parent('.comments').children('.comments-container').removeClass('hidden');
		
		/* Add class annotations-active to the parent with ID commentable-container */
		if(!$(this).parents("#commentable-container").hasClass('annotations-active')){
			$(this).parents("#commentable-container").addClass('annotations-active');
		}
	};
	
	/* Find all annotation toggle buttons and bind the click event to them. */
	$('.comments--toggle').on('click', annotations.toggleAnnotations );
	
	console.log('Binding complete');
});