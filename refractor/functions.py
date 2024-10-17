def process_scenario(network, edge_ids):
    """
    Deactivate edges, mark associated services as inactive, 
    and attempt to redirect the services.

    :param network: The Network object containing edges and services.
    :param edge_ids: A list of edge IDs to deactivate.
    :return: A tuple containing:
             - A list of service IDs that were successfully redirected.
             - The updated network.
    """
    redirected_services = []  # List to collect IDs of successfully redirected services
    deactivated_services = []  # List to collect all deactivated service IDs

    for edge_id in edge_ids:
        # Deactivate the edge and mark associated services as inactive
        try:
            # Deactivate the edge and get the associated services that were deactivated
            deactivated_services.extend(network.deactivate_edge(edge_id))  # Use .extend() for better performance
        except ValueError as e:
            # Raise an exception if the edge does not exist
            raise ValueError(f"Error: {e}")

    # After processing all edges, attempt to redirect the deactivated services
    for service_id in deactivated_services[:1]:
        service = network.services.get(service_id)
        # Check if the service is not dead and not active
        if service and not service.dead and not service.active:  
            # Attempt to redirect the service
            redirection = network.redirect_service(service)
            if redirection:  # Redirect the service
                network.remove_service_from_edges(service_id)  # Remove the service from edges
                network.services[service_id].path = redirection
                redirected_services.append(service_id)  # Add to redirected list
            else:
                service.mark_as_dead()  # Mark service as dead if redirection fails

    return redirected_services, network  # Return the list of redirected services and the updated network
